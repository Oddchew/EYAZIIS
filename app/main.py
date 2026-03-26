import os

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import unicodedata
import zipfile
import tempfile
from typing import Optional, List
import time

from app.database import engine, Base, get_db
from app.models import Document, Token
from app.schemas import (
    SearchQuery, SearchResponse, DocumentResponse, 
    DocumentStats, UpdateDocumentRequest, UploadFileRequest
)
from app.services.text_processor import TextProcessor
from app.services.morph_analyzer import MorphAnalyzer
from app.services.search_engine import SearchEngine
from app.config import settings

from sqlalchemy.sql import func

# Создаём таблицы БД
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Корпусный менеджер для лингвистического анализа текстов",
    version="1.0.0"
)

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация сервисов
morph_analyzer = MorphAnalyzer()


@app.get("/", tags=["Root"])
def read_root():
    """Информация о сервисе"""
    return {
        "name": settings.PROJECT_NAME,
        "docs": "/docs",  # Swagger UI
        "status": "running"
    }

import subprocess

@staticmethod
async def _read_doc(file_path: str) -> str:
    try:
        result = subprocess.run(
            ["antiword", file_path],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Не удалось извлечь текст из .doc файла: {e}")
    except FileNotFoundError:
        raise RuntimeError("Утилита 'antiword' не установлена. Выполните: sudo apt install antiword")

@app.post("/documents/upload", tags=["Documents"])
async def upload_document(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Загрузка нового текста в корпус"""
    import json
    
    # Валидация расширения
    ext = file.filename.split('.')[-1].lower()
    if f".{ext}" not in TextProcessor.SUPPORTED_FORMATS:
        raise HTTPException(400, f"Неподдерживаемый формат: .{ext}")
    
    # Сохраняем файл
    content = await file.read()
    filepath = TextProcessor.save_uploaded_file(content, file.filename)
    
    # Извлекаем текст
    text = await TextProcessor.extract_text(filepath, f".{ext}")
    
    # Парсим метаданные если есть
    meta_dict = json.loads(metadata) if metadata else {}
    
    # Создаём запись в БД
    doc = Document(
        filename=file.filename,
        filepath=filepath,
        content=text[:10000],  # Храним превью, полный текст в файле
        file_type=ext,
        meta_data=meta_dict
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    # Запускаем морфологическую обработку (в реальном проекте — в фоне через Celery)
    tokens = morph_analyzer.analyze_text(text, doc.id)
    db.add_all(tokens)
    doc.is_processed = True
    db.commit()
    
    return {"id": doc.id, "filename": doc.filename, "tokens_count": len(tokens)}


@app.get("/documents", response_model=List[DocumentResponse], tags=["Documents"])
def list_documents(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Список документов в корпусе"""
    docs = db.query(Document).offset(skip).limit(limit).all()
    return docs


@app.get("/documents/{doc_id}", response_model=DocumentResponse, tags=["Documents"])
def get_document(doc_id: int, with_stats: bool = False, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Документ не найден")

    response = DocumentResponse.model_validate(doc)

    if with_stats:
        response.stats = SearchEngine.get_document_stats(db, doc_id)

    return response


@app.delete("/documents/{doc_id}", tags=["Documents"])
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """Удаление документа из корпуса"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(404, "Документ не найден")
    
    # Удаляем файл если есть
    if doc.filepath:
        import os
        if os.path.exists(doc.filepath):
            os.remove(doc.filepath)
    
    db.delete(doc)
    db.commit()
    return {"status": "deleted", "id": doc_id}


# === Поиск и анализ ===

@app.post("/search", response_model=SearchResponse, tags=["Search"])
def search_corpus(query: SearchQuery, db: Session = Depends(get_db)):
    """
    Поиск по корпусу с поддержкой:
    - лемм, словоформ, частей речи, регулярных выражений
    - фильтров по документу и грамматическим признакам
    - настройки размера контекста
    """
    result = SearchEngine.search_concordances(db, query)
    return result

def normalize_lemma(lemma: str) -> str:
    return unicodedata.normalize('NFKC', lemma.strip().lower())

@app.get("/lemmas/{lemma}", tags=["Analysis"])
def get_lemma_info(lemma: str, db: Session = Depends(get_db)):
    """Частотная информация о лемме во всём корпусе"""
    
    # 1. Лемматизируем запрос через тот же анализатор, что и при индексации
    parsed = morph_analyzer.morph.parse(lemma)[0]  # доступ к экземпляру MorphAnalyzer
    query_lemma = parsed.normal_form  # "Шляпы" → "шляпа"
    
    # 2. Нормализуем для надёжного сравнения
    normalized = unicodedata.normalize('NFKC', query_lemma.strip())
    
    # 3. Ищем в БД (без func.lower, если леммы уже хранятся в нижнем регистре)
    tokens = db.query(Token).filter(
        Token.lemma == normalized
    ).all()
    
    if not tokens:
        # 🔍 Добавим подсказки для отладки
        debug_info = {
            "original_query": lemma,
            "lemmatized_query": query_lemma,
            "normalized_query": normalized,
            "sample_lemmas_in_db": [t.lemma for t in db.query(Token.lemma).distinct().limit(10).all()]
        }
        raise HTTPException(
            status_code=404, 
            detail={
                "error": f"Лемма '{lemma}' не найдена в корпусе",
                "debug": debug_info
            }
        )
    
    # ... остальная логика


@app.get("/stats/global", tags=["Statistics"])
def get_corpus_stats(db: Session = Depends(get_db)):
    """Общая статистика по всему корпусу"""
    total_docs = db.query(func.count(Document.id)).scalar()
    total_tokens = db.query(func.count(Token.id)).scalar()
    unique_lemmas = db.query(func.count(Token.lemma.distinct())).scalar()
    
    # Топ-20 лемм корпуса
    top_lemmas = db.query(Token.lemma, func.count(Token.id)).group_by(
        Token.lemma
    ).order_by(func.count(Token.id).desc()).limit(20).all()
    
    return {
        "total_documents": total_docs,
        "total_tokens": total_tokens,
        "unique_lemmas": unique_lemmas,
        "avg_tokens_per_doc": round(total_tokens / total_docs, 1) if total_docs else 0,
        "top_lemmas": [{"lemma": l, "count": c} for l, c in top_lemmas]
    }


# === Справка ===

@app.get("/help/api", tags=["Help"])
def api_help():
    """Справка по API (дублирует Swagger, но в формате JSON)"""
    return {
        "endpoints": {
            "POST /documents/upload": "Загрузка текста в корпус",
            "GET /documents": "Список документов",
            "GET /documents/{id}": "Информация о документе",
            "POST /search": "Поиск конкордансов",
            "GET /lemmas/{lemma}": "Статистика по лемме",
            "GET /stats/global": "Общая статистика корпуса"
        },
        "search_query_types": ["lemma", "word_form", "pos", "regex"],
        "supported_formats": list(TextProcessor.SUPPORTED_FORMATS.keys())
    }

@app.get("/documents/{doc_id}/download", tags=["Documents"])
def download_document(doc_id: int, db: Session = Depends(get_db)):
    """Скачать оригинальный файл документа"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc or not doc.filepath:
        raise HTTPException(status_code=404, detail="Файл документа не найден")
    
    if not os.path.exists(doc.filepath):
        raise HTTPException(status_code=500, detail="Файл на диске отсутствует")
    
    return FileResponse(
        path=doc.filepath,
        filename=doc.filename,
        media_type='application/octet-stream' # или более точный тип, если известен
    )

@app.get("/corpus/export", tags=["Documents"])
def export_corpus_archive(db: Session = Depends(get_db)):
    """Скачать архив со всеми документами корпуса"""
    docs = db.query(Document).all()
    
    if not docs:
        raise HTTPException(status_code=404, detail="Корпус пуст")

    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "corpus_export.zip")

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for doc in docs:
            if doc.filepath and os.path.exists(doc.filepath):
                zipf.write(doc.filepath, arcname=doc.filename)

    def cleanup():
        import shutil
        shutil.rmtree(temp_dir)

    import atexit
    atexit.register(cleanup)

    return FileResponse(
        path=zip_path,
        filename="corpus_export.zip",
        media_type='application/zip',
    )

@app.put("/documents/{doc_id}", response_model=DocumentResponse, tags=["Documents"])
def update_document(doc_id: int, request: UpdateDocumentRequest, db: Session = Depends(get_db)):
    """Обновить метаданные документа (имя файла, meta_data)"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Документ не найден")
    
    if request.filename is not None:
        doc.filename = request.filename
    if request.meta_data is not None:
        doc.meta_data = request.meta_data
    
    db.commit()
    db.refresh(doc)
    
    # Используем model_validate как в GET
    return DocumentResponse.model_validate(doc)