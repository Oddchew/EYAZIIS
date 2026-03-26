# app/schemas.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models import Document # <-- Добавим импорт модели

# === Запросы ===
class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, description="Поисковый запрос (слово или лемма)")
    query_type: str = Field(default="lemma", enum=["lemma", "word_form", "pos", "regex"])
    document_id: Optional[int] = None
    pos_filter: Optional[str] = None
    context_window: int = Field(default=5, ge=0, le=20)
    limit: int = Field(default=50, ge=1, le=500)


class UploadFileRequest(BaseModel):
    meta_data: Optional[Dict[str, Any]] = None


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
    left_context: str
    target: str
    right_context: str
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
    pos_distribution: Dict[str, int]
    top_lemmas: List[Dict[str, Any]]

    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    # Сделаем content_preview опциональным и сгенерируем его ниже
    content_preview: Optional[str] = None
    created_at: datetime
    is_processed: bool
    # meta_data: Optional[Dict[str, Any]] = {} # Добавьте, если нужно отображать
    stats: Optional[DocumentStats] = None

    class Config:
        from_attributes = True

    # Добавим валидатор для content_preview
    @field_validator('content_preview', mode='before')
    @classmethod
    def generate_content_preview(cls, v, info):
        # Если content_preview не был передан, пытаемся получить его из 'content' модели
        if v is None and info.data.get('content'): # info.data - словарь данных от ORM
            full_content = info.data.get('content')
            return full_content[:500] if full_content else ""
        # Если поле было передано явно, возвращаем его
        return v if v is not None else ""


class UpdateDocumentRequest(BaseModel):
    filename: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None