"""Токенизация и сегментация текста (EN / FR)."""

from __future__ import annotations

import re
from typing import List, Tuple

STOP_EN = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "to", "of",
    "in", "for", "on", "with", "at", "by", "from", "as", "into", "through",
    "during", "before", "after", "above", "below", "between", "under",
    "again", "further", "then", "once", "here", "there", "when", "where",
    "why", "how", "all", "each", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "just", "and", "but", "if", "or", "because", "until", "while",
    "about", "against", "up", "down", "out", "off", "over", "this", "that",
    "these", "those", "it", "its", "he", "she", "they", "we", "you", "i",
    "me", "my", "our", "your", "his", "her", "their", "what", "which", "who",
    "whom", "also", "both", "either", "neither", "one", "two", "any", "every",
}

STOP_FR = {
    "le", "la", "les", "un", "une", "des", "du", "de", "et", "ou", "mais",
    "donc", "car", "ni", "que", "qui", "quoi", "dont", "où", "ce", "cet",
    "cette", "ces", "mon", "ton", "son", "ma", "ta", "sa", "mes", "tes",
    "ses", "notre", "votre", "leur", "nos", "vos", "leurs", "je", "tu",
    "il", "elle", "nous", "vous", "ils", "elles", "on", "me", "te", "se",
    "lui", "y", "en", "ne", "pas", "plus", "moins", "très", "trop", "tout",
    "tous", "toute", "toutes", "avec", "sans", "sous", "sur", "dans", "par",
    "pour", "entre", "chez", "vers", "contre", "après", "avant", "pendant",
    "depuis", "jusque", "comme", "si", "quand", "lorsque", "puis", "alors",
    "aussi", "encore", "déjà", "ici", "là", "être", "avoir", "faire", "dit",
    "est", "sont", "était", "été", "aux", "au", "a", "à", "d", "l", "n", "s",
    "c", "qu", "il", "elle",
}

STOP = STOP_EN | STOP_FR


def tokenize(text: str, min_len: int = 2) -> List[str]:
    """
    Токены: только буквенные слова (unicode), без чисел и «чисто латинских»
    технических токенов из одной буквы. Стоп-слова отбрасываются.
    """
    text = text.lower()
    tokens = re.findall(r"[^\W\d_]+", text, flags=re.UNICODE)
    out = []
    for t in tokens:
        if len(t) < min_len:
            continue
        if t in STOP:
            continue
        # методичка: слова из латинских букв в общем учитываем для EN/FR
        out.append(t)
    return out


def split_sentences(text: str) -> List[str]:
    """Простое разбиение на предложения."""
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    # сохраняем конец предложения
    parts = re.split(r"(?<=[.!?…])\s+", text)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 15]


def split_paragraphs(text: str) -> List[str]:
    paras = re.split(r"\n\s*\n", text.strip())
    return [p.strip() for p in paras if p.strip()]


def sentence_offsets(text: str, sentences: List[str]) -> List[Tuple[int, int]]:
    """Позиции начала/конца предложений в исходном тексте (приближённо)."""
    offsets = []
    pos = 0
    lower = text
    for s in sentences:
        idx = lower.find(s, pos)
        if idx < 0:
            idx = pos
        offsets.append((idx, idx + len(s)))
        pos = idx + len(s)
    return offsets
