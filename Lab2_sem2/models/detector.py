"""
Единый фасад для распознавания языка тремя методами (вариант 7):
  - N-грамм (Out-of-Place)
  - Алфавитный
  - Нейросетевой
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .alphabet import AlphabetProfiler
from .ngrams import NGramProfiler, OutOfPlaceDistance
from .neural import NeuralLanguageClassifier
from .preprocess import extract_text_from_html, is_html_content, preprocess_text


SUPPORTED_LANGUAGES = ["english", "french"]
LANG_DISPLAY = {
    "english": "English (английский)",
    "french": "French (французский)",
}


@dataclass
class DetectionResult:
    method: str
    predicted: str
    distances_or_probs: Dict[str, float]
    elapsed_ms: float
    details: Dict = field(default_factory=dict)


class LanguageDetector:
    """Обучает профили на тренировочных текстах и классифицирует документы."""

    def __init__(self, model_dir: Optional[Path] = None):
        self.model_dir = Path(model_dir or Path(__file__).resolve().parent.parent / "data")
        self.model_dir.mkdir(parents=True, exist_ok=True)

        self.ngram_profiles: Dict[str, NGramProfiler] = {}
        self.alphabet_profiles: Dict[str, AlphabetProfiler] = {}
        self.neural = NeuralLanguageClassifier(hidden=48)
        self.oop = OutOfPlaceDistance()
        self.is_ready = False
        self.train_stats: Dict = {}

    # ------------------------------------------------------------------ train
    def train(
        self,
        corpus: Dict[str, List[str]],
        neural_epochs: int = 60,
    ) -> Dict:
        """
        corpus: {"english": [text1, text2, ...], "french": [...]}
        """
        t0 = time.perf_counter()
        self.ngram_profiles = {}
        self.alphabet_profiles = {}

        all_texts: List[str] = []
        all_labels: List[str] = []

        def _chunks(texts: List[str], size: int = 800) -> List[str]:
            """Разбивает длинные тексты на фрагменты для обучения MLP."""
            out: List[str] = []
            for t in texts:
                t = (t or "").strip()
                if not t:
                    continue
                if len(t) <= size:
                    out.append(t)
                else:
                    step = max(size // 2, 200)
                    for i in range(0, len(t), step):
                        part = t[i : i + size].strip()
                        if len(part) > 200:
                            out.append(part)
            return out

        for lang, texts in corpus.items():
            if lang not in SUPPORTED_LANGUAGES:
                continue
            clean = [t for t in texts if t and t.strip()]
            if not clean:
                continue
            # N-gram profile (на полных текстах)
            ng = NGramProfiler(max_n=5, profile_size=300)
            ng.build_from_texts(clean, language=lang)
            self.ngram_profiles[lang] = ng

            # Alphabet profile
            al = AlphabetProfiler()
            al.build_from_texts(clean, language=lang)
            self.alphabet_profiles[lang] = al

            for part in _chunks(clean):
                all_texts.append(part)
                all_labels.append(lang)

        neural_info = {}
        if all_texts:
            epochs = max(neural_epochs, 100)
            neural_info = self.neural.train(
                all_texts, all_labels, epochs=epochs, lr=0.06, verbose=False
            )
            model_path = self.model_dir / "neural_model.json"
            self.neural.save(model_path)

        elapsed = (time.perf_counter() - t0) * 1000
        self.is_ready = bool(self.ngram_profiles) and self.neural.trained
        self.train_stats = {
            "languages": list(self.ngram_profiles.keys()),
            "docs_per_lang": {k: len(v) for k, v in corpus.items()},
            "total_chars": {
                k: sum(len(t) for t in v) for k, v in corpus.items()
            },
            "neural": neural_info,
            "train_time_ms": round(elapsed, 1),
        }
        return self.train_stats

    def load_neural(self) -> bool:
        path = self.model_dir / "neural_model.json"
        if path.exists():
            self.neural.load(path)
            return True
        return False

    # ---------------------------------------------------------------- detect
    def _prepare_text(self, content: str) -> str:
        if is_html_content(content):
            content = extract_text_from_html(content)
        return content

    def detect_ngram(self, content: str) -> DetectionResult:
        text = self._prepare_text(content)
        t0 = time.perf_counter()
        doc = NGramProfiler(max_n=5, profile_size=300).build_from_text(text)
        best, dists = self.oop.classify(doc, self.ngram_profiles)
        elapsed = (time.perf_counter() - t0) * 1000
        return DetectionResult(
            method="N-грамм (Out-of-Place)",
            predicted=best,
            distances_or_probs={k: float(v) for k, v in dists.items()},
            elapsed_ms=round(elapsed, 3),
            details={"top_ngrams": doc.top(15)},
        )

    def detect_alphabet(self, content: str) -> DetectionResult:
        text = self._prepare_text(content)
        t0 = time.perf_counter()
        doc = AlphabetProfiler().build_from_text(text)
        best, dists = doc.classify(self.alphabet_profiles, metric="l1")
        elapsed = (time.perf_counter() - t0) * 1000
        return DetectionResult(
            method="Алфавитный",
            predicted=best,
            distances_or_probs={k: round(v, 6) for k, v in dists.items()},
            elapsed_ms=round(elapsed, 3),
            details={
                "marker_score": round(doc.marker_score, 5),
                "top_chars": sorted(doc.freqs.items(), key=lambda x: -x[1])[:12],
            },
        )

    def detect_neural(self, content: str) -> DetectionResult:
        text = self._prepare_text(content)
        t0 = time.perf_counter()
        best, probs = self.neural.predict(text)
        elapsed = (time.perf_counter() - t0) * 1000
        return DetectionResult(
            method="Нейросетевой (MLP)",
            predicted=best,
            distances_or_probs={k: round(v, 6) for k, v in probs.items()},
            elapsed_ms=round(elapsed, 3),
            details={},
        )

    def detect_all(self, content: str) -> List[DetectionResult]:
        if not self.is_ready:
            raise RuntimeError("Detector is not trained. Call train() first.")
        return [
            self.detect_ngram(content),
            self.detect_alphabet(content),
            self.detect_neural(content),
        ]

    def majority_vote(self, results: List[DetectionResult]) -> str:
        from collections import Counter
        votes = Counter(r.predicted for r in results)
        return votes.most_common(1)[0][0]
