"""Совместимость: реэкспорт из модулей."""

from models.document import Document, tokenize, STOP_WORDS
from models.index import InvertedIndex
from models.search import BooleanSearchEngine
from models.metrics import MetricsEvaluator
from data.collection import DOCUMENTS, RELEVANCE_JUDGMENTS

__all__ = [
    "Document",
    "tokenize",
    "STOP_WORDS",
    "InvertedIndex",
    "BooleanSearchEngine",
    "MetricsEvaluator",
    "DOCUMENTS",
    "RELEVANCE_JUDGMENTS",
]
