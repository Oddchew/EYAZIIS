#!/usr/bin/env python3
"""Консольный режим поиска."""

import json
from models.index import InvertedIndex
from models.search import BooleanSearchEngine
from models.metrics import MetricsEvaluator
from models.storage import DocumentStore
from data.collection import RELEVANCE_JUDGMENTS


def print_table(metrics_list):
    print("-" * 90)
    print(f"{'query':<40} {'P':>6} {'R':>6} {'F1':>6} {'P@5':>6} {'AP':>6}")
    print("-" * 90)
    for m in metrics_list:
        q = m["query"][:37] + "..." if len(m["query"]) > 40 else m["query"]
        print(
            f"{q:<40} {m['precision']:>6.3f} {m['recall']:>6.3f} "
            f"{m['f_measure']:>6.3f} {m['precision_at_5']:>6.3f} "
            f"{m['average_precision']:>6.3f}"
        )
    n = len(metrics_list) or 1
    avg_p = sum(m["precision"] for m in metrics_list) / n
    avg_r = sum(m["recall"] for m in metrics_list) / n
    avg_f = sum(m["f_measure"] for m in metrics_list) / n
    avg_ap = sum(m["average_precision"] for m in metrics_list) / n
    print("-" * 90)
    print(f"{'avg':<40} {avg_p:>6.3f} {avg_r:>6.3f} {avg_f:>6.3f} {'':>6} {avg_ap:>6.3f}")
    print("-" * 90)


def main():
    print("ИПС Boolean search")
    store = DocumentStore()
    if store.is_empty():
        from data.collection import DOCUMENTS
        store.load_from_dict(DOCUMENTS)
        print("БД была пуста — загружена стартовая коллекция")

    index = InvertedIndex()
    index.build_from_dict(store.get_all())
    print(f"документов: {index.N}, терминов: {len(index.index)}")
    print(f"БД: {store.db_path}")

    engine = BooleanSearchEngine(index)
    evaluator = MetricsEvaluator(RELEVANCE_JUDGMENTS)

    print("\nоценка:")
    metrics = evaluator.evaluate_all(engine)
    print_table(metrics)

    with open("metrics_results.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    print("\nпоиск (AND/OR/NOT), quit — выход, eval — метрики")
    while True:
        try:
            query = input("\nзапрос> ").strip()
            if not query:
                continue
            if query.lower() == "quit":
                break
            if query.lower() == "eval":
                print_table(evaluator.evaluate_all(engine))
                continue
            results = engine.search(query)
            if not results:
                print("ничего не найдено")
            else:
                print(f"найдено: {len(results)}")
                for i, r in enumerate(results, 1):
                    print(f"{i}. [{r['documentId']}] {r['title']}")
                    print(f"   {r['snippet'][:100]}...")
                    print(f"   совпало: {', '.join(r['matched_terms'])}")
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    main()
