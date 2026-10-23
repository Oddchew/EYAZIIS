"""
Алфавитный метод распознавания языка.

ПОЯ — распределение частот символов алфавита (и характерных диакритических
знаков). Расстояние между профилями — сумма абсолютных разностей
относительных частот (L1) или косинусное расстояние.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, List, Optional, Tuple

from .preprocess import preprocess_text

# Характерные буквы / диакритика для французского и английского
# (для расширения на другие языки легко добавить)
LANGUAGE_ALPHABETS: Dict[str, set] = {
    "english": set("abcdefghijklmnopqrstuvwxyz"),
    "french": set(
        "abcdefghijklmnopqrstuvwxyz"
        "àâäæçéèêëïîôœùûüÿ"
        "àâäæçéèêëïîôœùûüÿ".upper()  # на случай если lower не сработал
    ),
}

# Уникальные для французского символы (сильный сигнал)
FRENCH_MARKERS = set("àâäæçéèêëïîôœùûüÿ")


def char_frequencies(text: str) -> Dict[str, float]:
    """Относительные частоты букв (только буквы, lowercase)."""
    text = preprocess_text(text, keep_spaces=False)
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return {}
    total = len(letters)
    cnt = Counter(letters)
    return {ch: freq / total for ch, freq in cnt.items()}


class AlphabetProfiler:
    """Профиль языка / документа по частотам символов."""

    def __init__(self):
        self.freqs: Dict[str, float] = {}
        self.language: Optional[str] = None
        self.marker_score: float = 0.0  # доля характерных фр. символов

    def build_from_text(self, text: str, language: Optional[str] = None) -> "AlphabetProfiler":
        self.freqs = char_frequencies(text)
        self.language = language
        total_letters = sum(1 for c in preprocess_text(text, keep_spaces=False) if c.isalpha())
        if total_letters > 0:
            markers = sum(
                1
                for c in preprocess_text(text, keep_spaces=False)
                if c in FRENCH_MARKERS
            )
            self.marker_score = markers / total_letters
        else:
            self.marker_score = 0.0
        return self

    def build_from_texts(self, texts: List[str], language: Optional[str] = None) -> "AlphabetProfiler":
        return self.build_from_text(" ".join(texts), language)

    def l1_distance(self, other: "AlphabetProfiler") -> float:
        """Сумма |p - q| по всем символам (L1)."""
        keys = set(self.freqs) | set(other.freqs)
        return sum(abs(self.freqs.get(k, 0.0) - other.freqs.get(k, 0.0)) for k in keys)

    def cosine_distance(self, other: "AlphabetProfiler") -> float:
        """1 - cosine similarity (0 = identical)."""
        keys = set(self.freqs) | set(other.freqs)
        if not keys:
            return 1.0
        dot = sum(self.freqs.get(k, 0.0) * other.freqs.get(k, 0.0) for k in keys)
        n1 = sum(v * v for v in self.freqs.values()) ** 0.5
        n2 = sum(v * v for v in other.freqs.values()) ** 0.5
        if n1 == 0 or n2 == 0:
            return 1.0
        return 1.0 - (dot / (n1 * n2))

    def classify(
        self,
        language_profiles: Dict[str, "AlphabetProfiler"],
        metric: str = "l1",
    ) -> Tuple[str, Dict[str, float]]:
        distances: Dict[str, float] = {}
        for lang, profile in language_profiles.items():
            if metric == "cosine":
                distances[lang] = self.cosine_distance(profile)
            else:
                distances[lang] = self.l1_distance(profile)
        # Дополнительный бонус/штраф по маркерам для французского
        # (если в документе много diacritics — ближе к french)
        if "french" in distances and self.marker_score > 0.005:
            distances["french"] *= max(0.3, 1.0 - self.marker_score * 15)
        if "english" in distances and self.marker_score > 0.01:
            distances["english"] *= 1.0 + self.marker_score * 10
        best = min(distances, key=distances.get)  # type: ignore
        return best, distances
