"""
Элементы ИИ в пользовательском интерфейсе.
- подсказки терминов из словаря индекса
- подсветка совпавших слов в фрагменте
- связанные термины (совместная встречаемость)
"""

from typing import List, Dict, Set
from models.index import InvertedIndex
from models.document import tokenize


def suggest_terms(index: InvertedIndex, prefix: str, limit: int = 8) -> List[str]:
    """Автодополнение по префиксу из словаря индекса."""
    prefix = prefix.lower().strip()
    if len(prefix) < 2:
        return []
    matches = [t for t in index.index.keys() if t.startswith(prefix)]
    # чаще встречающиеся — выше
    matches.sort(key=lambda t: (-index.df.get(t, 0), t))
    return matches[:limit]


def highlight_snippet(text: str, terms: List[str], max_len: int = 280) -> str:
    """Подсветка терминов запроса в сниппете (для HTML)."""
    import re
    import html as html_mod

    snippet = text[:max_len]
    if len(text) > max_len:
        snippet = snippet.rsplit(" ", 1)[0] + "..."

    escaped = html_mod.escape(snippet)
    for term in sorted(set(terms), key=len, reverse=True):
        if not term:
            continue
        pattern = re.compile(re.escape(html_mod.escape(term)), re.IGNORECASE)
        escaped = pattern.sub(
            lambda m: f'<mark>{m.group(0)}</mark>',
            escaped,
        )
    return escaped


def related_terms(index: InvertedIndex, query: str, limit: int = 6) -> List[Dict]:
    """
    Связанные термины: слова, часто встречающиеся
    в тех же документах, что и термины запроса.
    """
    q_terms = [
        t for t in tokenize(query)
        if t not in ("and", "or", "not")
    ]
    if not q_terms:
        return []

    # документы, покрытые запросом (OR по терминам)
    docs: Set[int] = set()
    for t in q_terms:
        docs |= index.get_postings(t)
    if not docs:
        return []

    # считаем частоты других терминов в этих документах
    co_freq: Dict[str, int] = {}
    q_set = set(q_terms)
    for doc_id in docs:
        doc = index.documents.get(doc_id)
        if not doc:
            continue
        for term in set(doc.tokens):
            if term in q_set:
                continue
            co_freq[term] = co_freq.get(term, 0) + 1

    ranked = sorted(co_freq.items(), key=lambda x: (-x[1], x[0]))
    return [{"term": t, "docs": c} for t, c in ranked[:limit]]


def query_hints(index: InvertedIndex) -> List[str]:
    """Примеры запросов на основе частых терминов коллекции."""
    top = sorted(index.df.items(), key=lambda x: -x[1])[:12]
    terms = [t for t, _ in top]
    hints = []
    if len(terms) >= 2:
        hints.append(f"{terms[0]} AND {terms[1]}")
        hints.append(f"{terms[0]} OR {terms[2] if len(terms) > 2 else terms[1]}")
    if len(terms) >= 3:
        hints.append(f"{terms[1]} AND {terms[2]} NOT {terms[0]}")
    return hints
