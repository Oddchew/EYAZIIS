"""
Метод N-грамм (Cavnar & Trenkle, 1994).
Профиль языка / документа — отсортированный список N-грамм (N=1..5)
по убыванию частоты. Расстояние — Out-Of-Place measure.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, List, Optional, Tuple

from .preprocess import preprocess_text


DEFAULT_N = 5
DEFAULT_PROFILE_SIZE = 300  # ~300 самых частых N-грамм
MAX_OUT_OF_PLACE = 1000  # штраф за отсутствие N-граммы в профиле


def generate_ngrams(text: str, max_n: int = DEFAULT_N) -> List[str]:
    """
    Генерирует все N-граммы длины 1..max_n.
    Пробелы заменяются на '_' (как в оригинальной работе TextCat),
    чтобы границы слов тоже учитывались.
    """
    text = preprocess_text(text, keep_spaces=True)
    if not text:
        return []
    # padding with underscores for word boundaries
    padded = f"_{text.replace(' ', '_')}_"
    ngrams: List[str] = []
    length = len(padded)
    for n in range(1, max_n + 1):
        for i in range(length - n + 1):
            gram = padded[i : i + n]
            ngrams.append(gram)
    return ngrams


class NGramProfiler:
    """Строит и хранит профиль частот N-грамм."""

    def __init__(
        self,
        max_n: int = DEFAULT_N,
        profile_size: int = DEFAULT_PROFILE_SIZE,
    ):
        self.max_n = max_n
        self.profile_size = profile_size
        self.rank: Dict[str, int] = {}  # ngram -> rank (0 = most frequent)
        self.ordered: List[str] = []  # sorted by frequency desc
        self.counts: Counter = Counter()
        self.language: Optional[str] = None

    def build_from_text(self, text: str, language: Optional[str] = None) -> "NGramProfiler":
        ngrams = generate_ngrams(text, self.max_n)
        self.counts = Counter(ngrams)
        # sort by frequency descending, then by ngram for stability
        ordered = sorted(self.counts.items(), key=lambda x: (-x[1], x[0]))
        self.ordered = [g for g, _ in ordered[: self.profile_size]]
        self.rank = {g: i for i, g in enumerate(self.ordered)}
        self.language = language
        return self

    def build_from_texts(self, texts: List[str], language: Optional[str] = None) -> "NGramProfiler":
        combined = " ".join(texts)
        return self.build_from_text(combined, language)

    def top(self, k: int = 20) -> List[Tuple[str, int]]:
        return [(g, self.counts[g]) for g in self.ordered[:k]]


class OutOfPlaceDistance:
    """Метрика несовпадения позиций (Out-Of-Place) между двумя профилями."""

    def __init__(self, max_penalty: int = MAX_OUT_OF_PLACE):
        self.max_penalty = max_penalty

    def distance(self, doc_profile: NGramProfiler, lang_profile: NGramProfiler) -> int:
        """
        Для каждой N-граммы из профиля документа берём |rank_doc - rank_lang|.
        Если N-граммы нет в профиле языка — max_penalty.
        """
        total = 0
        for gram, doc_rank in doc_profile.rank.items():
            if gram in lang_profile.rank:
                total += abs(doc_rank - lang_profile.rank[gram])
            else:
                total += self.max_penalty
        return total

    def classify(
        self,
        doc_profile: NGramProfiler,
        language_profiles: Dict[str, NGramProfiler],
    ) -> Tuple[str, Dict[str, int]]:
        """Возвращает язык с минимальным расстоянием и словарь всех расстояний."""
        distances: Dict[str, int] = {}
        for lang, profile in language_profiles.items():
            distances[lang] = self.distance(doc_profile, profile)
        best = min(distances, key=distances.get)  # type: ignore
        return best, distances
