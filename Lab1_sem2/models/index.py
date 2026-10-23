"""Инвертированный индекс."""

from collections import defaultdict
from typing import Dict, Set
from models.document import Document


class InvertedIndex:
    def __init__(self):
        self.index: Dict[str, Set[int]] = defaultdict(set)
        self.documents: Dict[int, Document] = {}
        self.N = 0
        # df: сколько документов содержат термин (для idf)
        self.df: Dict[str, int] = defaultdict(int)

    def add_document(self, doc: Document):
        if doc.doc_id in self.documents:
            return
        self.documents[doc.doc_id] = doc
        self.N += 1
        seen = set()
        for token in doc.tokens:
            self.index[token].add(doc.doc_id)
            if token not in seen:
                self.df[token] += 1
                seen.add(token)

    def get_postings(self, term: str) -> Set[int]:
        return set(self.index.get(term.lower(), set()))

    def idf(self, term: str) -> float:
        """Инверсная частота термина: Bi = log(N / Pi) — формула (1.5)."""
        import math
        pi = self.df.get(term.lower(), 0)
        if pi == 0 or self.N == 0:
            return 0.0
        return math.log(self.N / pi)

    def term_weight(self, term: str, doc_id: int) -> float:
        """Вес термина в документе: Aj = Qj * Bi — формула (1.6)."""
        doc = self.documents.get(doc_id)
        if not doc:
            return 0.0
        q = doc.term_freq.get(term.lower(), 0)
        return q * self.idf(term)

    def build_from_dict(self, docs_dict: dict):
        for doc_id, data in docs_dict.items():
            doc = Document(
                doc_id,
                data["title"],
                data["text"],
                data.get("date", "2026-01-01"),
            )
            self.add_document(doc)

    def all_doc_ids(self) -> Set[int]:
        return set(self.documents.keys())
