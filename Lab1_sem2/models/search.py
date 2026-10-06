"""Boolean-поиск."""

import re
from typing import List, Dict, Set
from models.index import InvertedIndex
from models.document import tokenize


class BooleanSearchEngine:
    def __init__(self, index: InvertedIndex):
        self.index = index

    def _parse(self, query: str) -> List:
        query = query.lower().strip()
        return re.findall(r"\b(?:and|or|not)\b|\b[a-z]+\b|\(|\)", query)

    def _evaluate(self, tokens: List) -> Set[int]:
        if not tokens:
            return set()

        # NOT term
        i = 0
        processed = []
        while i < len(tokens):
            t = tokens[i]
            if t == "not" and i + 1 < len(tokens):
                nxt = tokens[i + 1]
                if nxt not in ("and", "or", "not", "(", ")"):
                    postings = self.index.get_postings(nxt)
                    processed.append(self.index.all_doc_ids() - postings)
                    i += 2
                    continue
            processed.append(t)
            i += 1

        # terms -> postings
        items = []
        for t in processed:
            if isinstance(t, set):
                items.append(t)
            elif t in ("and", "or", "not", "(", ")"):
                items.append(t)
            else:
                items.append(self.index.get_postings(t))

        if not items:
            return set()

        result = items[0] if isinstance(items[0], set) else set()
        i = 1
        while i < len(items):
            op = items[i]
            if i + 1 >= len(items):
                break
            right = items[i + 1] if isinstance(items[i + 1], set) else set()
            if op == "and":
                result = result & right
            elif op == "or":
                result = result | right
            i += 2
        return result if isinstance(result, set) else set()

    def search(self, query: str) -> List[Dict]:
        tokens = self._parse(query)
        doc_ids = sorted(self._evaluate(tokens))
        query_terms = [
            t for t in re.findall(r"\b[a-z]+\b", query.lower())
            if t not in ("and", "or", "not")
        ]
        results = []
        for doc_id in doc_ids:
            doc = self.index.documents[doc_id]
            matched = doc.matched_terms(query_terms)
            # веса совпавших терминов (формула 1.6)
            weights = {
                t: round(self.index.term_weight(t, doc_id), 4)
                for t in matched
            }
            results.append({
                "documentId": doc.doc_id,
                "title": doc.title,
                "snippet": doc.snippet(),
                "matched_terms": matched,
                "weights": weights,
                "date": doc.date,
                "rank": 1.0,
            })
        return results
