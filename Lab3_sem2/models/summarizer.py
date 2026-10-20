"""
Автоматическое реферирование:
  1) классический реферат — sentence extraction (формулы из методички);
  2) реферат в виде ключевых слов (плоский + иерархический);
  3) тематическая группировка предложений (вместо OSTIS) —
     кластеры по совместной встречаемости терминов.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .preprocess import (
    sentence_offsets,
    split_paragraphs,
    split_sentences,
    tokenize,
)


@dataclass
class SentenceInfo:
    index: int
    text: str
    tokens: List[str]
    start: int
    end: int
    para_index: int
    score: float = 0.0
    posd: float = 0.0
    posp: float = 0.0
    tfidf_score: float = 0.0


@dataclass
class SummaryResult:
    title: str
    language: str
    source_id: str
    classical: List[str]  # выбранные предложения (порядок текста)
    keywords_flat: List[Tuple[str, float]]  # term, weight
    keywords_tree: Dict[str, List[str]]  # корень -> потомки
    topic_groups: List[Dict]  # тематические группы
    sentence_scores: List[Dict] = field(default_factory=list)
    stats: Dict = field(default_factory=dict)


class DocumentSummarizer:
    """
    Sentence extraction + ключевые слова + тематическая структура.

    Вес предложения:
        weight(S_i) = Posd(S_i) * Posp(S_i) * Score(S_i)

    Posd(S_i) = 1 - BD(S_i) / |D|
    Posp(S_i) = 1 - BP(S_i) / |P|

    Score(S_i) = sum_{t in S_i} tf(t, S_i) * w(t, D)
    w(t, D) = 0.5 * (1 + tf(t,D)/tfmax(D)) * log(|DB| / df(t))
    """

    def __init__(self, max_sentences: int = 10, max_keywords: int = 20):
        self.max_sentences = max_sentences
        self.max_keywords = max_keywords
        # корпус для df (обновляется при add_document / build_from_collection)
        self.doc_freq: Counter = Counter()
        self.n_docs: int = 0
        self._docs_tokens: List[List[str]] = []

    # ------------------------------------------------------------------ corpus
    def fit_collection(self, texts: List[str]) -> None:
        """Оценка df по коллекции документов."""
        self.doc_freq = Counter()
        self._docs_tokens = []
        for text in texts:
            terms = set(tokenize(text))
            self._docs_tokens.append(list(terms))
            for t in terms:
                self.doc_freq[t] += 1
        self.n_docs = max(len(texts), 1)

    def _ensure_df(self, tokens: List[str]) -> None:
        """Если коллекция пуста — работаем как с одним документом (|DB|=1)."""
        if self.n_docs == 0:
            self.n_docs = 1
            for t in set(tokens):
                self.doc_freq[t] = 1

    # ------------------------------------------------------------------ weights
    def _term_weights(self, doc_tokens: List[str]) -> Dict[str, float]:
        tf = Counter(doc_tokens)
        if not tf:
            return {}
        tfmax = max(tf.values())
        db = max(self.n_docs, 1)
        weights = {}
        for t, f in tf.items():
            df = self.doc_freq.get(t, 1)
            idf = math.log(db / df) if df > 0 else 0.0
            # если один документ, idf=0 — используем сглаженный вариант
            if self.n_docs <= 1:
                idf = math.log(1.0 + tfmax / f)  # локальная значимость
            w = 0.5 * (1.0 + f / tfmax) * max(idf, 0.1)
            weights[t] = w
        return weights

    def _build_sentences(self, text: str) -> List[SentenceInfo]:
        paragraphs = split_paragraphs(text)
        if not paragraphs:
            paragraphs = [text]

        sentences: List[SentenceInfo] = []
        # глобальные смещения
        full = text
        sent_list = split_sentences(full)
        offsets = sentence_offsets(full, sent_list)
        doc_len = max(len(full), 1)

        # привязка к абзацам
        para_ranges = []
        pos = 0
        for p in paragraphs:
            idx = full.find(p, pos)
            if idx < 0:
                idx = pos
            para_ranges.append((idx, idx + len(p), p))
            pos = idx + len(p)

        def para_of(start: int) -> Tuple[int, str]:
            for i, (a, b, p) in enumerate(para_ranges):
                if a <= start < b or start < b:
                    return i, p
            return 0, paragraphs[0]

        for i, (sent, (st, en)) in enumerate(zip(sent_list, offsets)):
            pi, para = para_of(st)
            para_len = max(len(para), 1)
            # BD — символы до предложения в документе
            bd = st
            # BP — символы до предложения в абзаце
            para_start = para_ranges[pi][0] if pi < len(para_ranges) else 0
            bp = max(st - para_start, 0)

            posd = 1.0 - bd / doc_len
            posp = 1.0 - bp / para_len
            # небольшой бонус первым предложениям абзаца
            tokens = tokenize(sent)
            sentences.append(
                SentenceInfo(
                    index=i,
                    text=sent,
                    tokens=tokens,
                    start=st,
                    end=en,
                    para_index=pi,
                    posd=max(posd, 0.05),
                    posp=max(posp, 0.05),
                )
            )
        return sentences

    def _score_sentences(
        self, sentences: List[SentenceInfo], term_w: Dict[str, float]
    ) -> None:
        for s in sentences:
            tf_s = Counter(s.tokens)
            score_tfidf = sum(tf_s[t] * term_w.get(t, 0.0) for t in tf_s)
            s.tfidf_score = score_tfidf
            s.score = s.posd * s.posp * score_tfidf

    # ------------------------------------------------------------------ keywords
    def extract_keywords(
        self, doc_tokens: List[str], term_w: Dict[str, float]
    ) -> List[Tuple[str, float]]:
        tf = Counter(doc_tokens)
        scored = []
        for t, f in tf.items():
            scored.append((t, term_w.get(t, 0.0) * f))
        scored.sort(key=lambda x: -x[1])
        return scored[: self.max_keywords]

    def keyword_tree(
        self, keywords: List[Tuple[str, float]], doc_tokens: List[str]
    ) -> Dict[str, List[str]]:
        """
        Иерархия: более короткое слово-корень «поглощает» составные/длинные
        термины, в которых оно встречается как подстрока (именные группы).
        """
        terms = [t for t, _ in keywords]
        roots: Dict[str, List[str]] = {}
        used = set()
        # сортируем короткие сначала
        ordered = sorted(terms, key=lambda x: (len(x), x))
        for t in ordered:
            if t in used:
                continue
            children = []
            for u in terms:
                if u == t or u in used:
                    continue
                if t in u and len(u) > len(t):
                    children.append(u)
                    used.add(u)
            roots[t] = sorted(children)
            used.add(t)
        # оставим только корни с весом из исходного списка
        return {k: v for k, v in roots.items() if k in terms}

    # ------------------------------------------------------------------ topics (вместо OSTIS)
    def topic_groups(
        self,
        sentences: List[SentenceInfo],
        keywords: List[Tuple[str, float]],
        max_groups: int = 5,
    ) -> List[Dict]:
        """
        Тематическая группировка: каждый топ-термин — «узел», предложения
        привязываются к термину с максимальным покрытием. Аналог простой
        концептуальной структуры (без OSTIS).
        """
        top_terms = [t for t, _ in keywords[:max_groups]]
        groups: Dict[str, List[str]] = {t: [] for t in top_terms}
        unassigned = []

        for s in sentences:
            if not s.tokens:
                continue
            best, best_hit = None, 0
            for t in top_terms:
                hit = s.tokens.count(t)
                if hit > best_hit:
                    best_hit = hit
                    best = t
            if best and best_hit > 0:
                groups[best].append(s.text)
            else:
                unassigned.append(s.text)

        result = []
        for t in top_terms:
            if groups[t]:
                result.append(
                    {
                        "topic": t,
                        "sentences": groups[t][:3],
                        "count": len(groups[t]),
                    }
                )
        if unassigned:
            result.append(
                {
                    "topic": "other",
                    "sentences": unassigned[:2],
                    "count": len(unassigned),
                }
            )
        return result

    # ------------------------------------------------------------------ main
    def summarize(
        self,
        text: str,
        title: str = "",
        language: str = "unknown",
        source_id: str = "",
        max_sentences: Optional[int] = None,
    ) -> SummaryResult:
        max_s = max_sentences or self.max_sentences
        doc_tokens = tokenize(text)
        self._ensure_df(doc_tokens)
        term_w = self._term_weights(doc_tokens)

        sentences = self._build_sentences(text)
        self._score_sentences(sentences, term_w)

        # выбор top-N по весу, затем восстановление порядка текста
        ranked = sorted(sentences, key=lambda s: -s.score)
        # отсекаем слишком короткие / пустые по токенам
        ranked = [s for s in ranked if len(s.tokens) >= 3]
        selected = ranked[:max_s]
        selected_sorted = sorted(selected, key=lambda s: s.index)
        classical = [s.text for s in selected_sorted]

        keywords = self.extract_keywords(doc_tokens, term_w)
        tree = self.keyword_tree(keywords, doc_tokens)
        topics = self.topic_groups(sentences, keywords)

        sent_scores = [
            {
                "index": s.index,
                "score": round(s.score, 4),
                "posd": round(s.posd, 4),
                "posp": round(s.posp, 4),
                "tfidf": round(s.tfidf_score, 4),
                "selected": s in selected,
                "preview": s.text[:100] + ("…" if len(s.text) > 100 else ""),
            }
            for s in sentences
        ]

        return SummaryResult(
            title=title or "document",
            language=language,
            source_id=source_id or title or "doc",
            classical=classical,
            keywords_flat=keywords,
            keywords_tree=tree,
            topic_groups=topics,
            sentence_scores=sent_scores,
            stats={
                "chars": len(text),
                "sentences": len(sentences),
                "selected": len(classical),
                "tokens": len(doc_tokens),
                "unique_terms": len(set(doc_tokens)),
            },
        )
