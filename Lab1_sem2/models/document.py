"""Документ и токенизация."""

import re
from typing import List

STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need",
    "to", "of", "in", "for", "on", "with", "at", "by", "from", "as",
    "into", "through", "during", "before", "after", "above", "below",
    "between", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how", "all", "each", "few",
    "more", "most", "other", "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very", "just", "and", "but", "if",
    "or", "because", "until", "while", "about", "against", "up", "down",
    "out", "off", "over", "this", "that", "these", "those", "it", "its",
}


def tokenize(text: str) -> List[str]:
    text = text.lower()
    tokens = re.findall(r"\b[a-z]+\b", text)
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


class Document:
    def __init__(self, doc_id: int, title: str, text: str, date: str = ""):
        self.doc_id = doc_id
        self.title = title
        self.text = text
        self.date = date or "2026-01-01"
        self.tokens = tokenize(title + " " + text)
        # частоты терминов в документе (для весов по формуле 1.6)
        self.term_freq = {}
        for t in self.tokens:
            self.term_freq[t] = self.term_freq.get(t, 0) + 1

    def snippet(self, max_len: int = 250) -> str:
        if len(self.text) <= max_len:
            return self.text
        return self.text[:max_len].rsplit(" ", 1)[0] + "..."

    def matched_terms(self, query_terms: List[str]) -> List[str]:
        doc_set = set(self.tokens)
        return [t for t in query_terms if t in doc_set]
