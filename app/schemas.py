from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# === Запросы ===
class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, description="Поисковый запрос (слово или лемма)")
    query_type: str = Field(default="lemma", enum=["lemma", "word_form", "pos", "regex"])
    document_id: Optional[int] = None  # Фильтр по документу
    pos_filter: Optional[str] = None   # Фильтр по части речи, например "VERB"
    context_window: int = Field(default=5, ge=0, le=20)  # Слов контекста слева/справа
    limit: int = Field(default=50, ge=1, le=500)


class UploadFileRequest(BaseModel):
    meta_data: Optional[Dict[str, Any]] = None  # Дополнительные метаданные


# === Ответы ===
class TokenResponse(BaseModel):
    word_form: str
    lemma: str
    pos: str
    grammemes: List[str]
    position: int
    
    class Config:
        from_attributes = True


class ConcordanceItem(BaseModel):
    document_id: int
    filename: str
    position: int
    left_context: str  # Текст слева от вхождения
    target: str        # Найденное слово
    right_context: str # Текст справа
    grammemes: List[str]
    
    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    query: str
    total_found: int
    results: List[ConcordanceItem]
    execution_time_ms: float


class DocumentStats(BaseModel):
    document_id: int
    filename: str
    total_tokens: int
    unique_lemmas: int
    pos_distribution: Dict[str, int]  # {"VERB": 120, "NOUN": 340, ...}
    top_lemmas: List[Dict[str, Any]]  # [{"lemma": "быть", "count": 45}, ...]


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    content_preview: str
    created_at: datetime
    is_processed: bool
    meta_data: Optional[Dict[str, Any]] = {}  # Добавляем это поле
    stats: Optional[DocumentStats] = None
    
    class Config:
        from_attributes = True