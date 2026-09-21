"""Метрики качества ROMIP / TREC."""

from typing import List, Dict, Set
from models.search import BooleanSearchEngine


class MetricsEvaluator:
    def __init__(self, relevance: Dict[str, Set[int]]):
        self.relevance = relevance

    def precision(self, retrieved: Set[int], relevant: Set[int]) -> float:
        if not retrieved:
            return 0.0
        return len(retrieved & relevant) / len(retrieved)

    def recall(self, retrieved: Set[int], relevant: Set[int]) -> float:
        if not relevant:
            return 0.0
        return len(retrieved & relevant) / len(relevant)

    def f_measure(self, p: float, r: float) -> float:
        if p + r == 0:
            return 0.0
        return 2 * p * r / (p + r)

    def precision_at_k(self, retrieved_list: List[int], relevant: Set[int], k: int) -> float:
        top_k = set(retrieved_list[:k])
        if not top_k:
            return 0.0
        return len(top_k & relevant) / min(k, len(retrieved_list) or 1)

    def average_precision(self, retrieved_list: List[int], relevant: Set[int]) -> float:
        if not relevant:
            return 0.0
        score = 0.0
        hits = 0
        for i, doc_id in enumerate(retrieved_list, 1):
            if doc_id in relevant:
                hits += 1
                score += hits / i
        return score / len(relevant)

    def r_precision(self, retrieved_list: List[int], relevant: Set[int]) -> float:
        r = len(relevant)
        if r == 0:
            return 0.0
        top_r = set(retrieved_list[:r])
        return len(top_r & relevant) / r

    def evaluate_query(self, query: str, retrieved_list: List[int]) -> Dict:
        relevant = self.relevance.get(query, set())
        retrieved_set = set(retrieved_list)
        p = self.precision(retrieved_set, relevant)
        r = self.recall(retrieved_set, relevant)
        return {
            "query": query,
            "precision": round(p, 4),
            "recall": round(r, 4),
            "f_measure": round(self.f_measure(p, r), 4),
            "precision_at_5": round(self.precision_at_k(retrieved_list, relevant, 5), 4),
            "precision_at_10": round(self.precision_at_k(retrieved_list, relevant, 10), 4),
            "average_precision": round(self.average_precision(retrieved_list, relevant), 4),
            "r_precision": round(self.r_precision(retrieved_list, relevant), 4),
            "num_relevant": len(relevant),
            "num_retrieved": len(retrieved_list),
            "num_relevant_retrieved": len(retrieved_set & relevant),
        }

    def evaluate_all(self, engine: BooleanSearchEngine) -> List[Dict]:
        results = []
        for query in self.relevance:
            search_results = engine.search(query)
            retrieved_list = [r["documentId"] for r in search_results]
            results.append(self.evaluate_query(query, retrieved_list))
        return results
