#!/usr/bin/env python3
"""
Автоматическое реферирование документов.
Вариант 7: FR / EN, computer science + литература.
Метод: sentence extraction (формулы методички) + ключевые слова
+ тематическая группировка (вместо OSTIS).
"""

from __future__ import annotations

import io
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from data.collection import get_document, get_documents
from models.summarizer import DocumentSummarizer

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)

app = FastAPI(title="Реферирование документов", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE / "templates"))

summarizer = DocumentSummarizer(max_sentences=10, max_keywords=18)
history: List[dict] = []
HISTORY_FILE = DATA / "history.json"


def _load_history():
    global history
    if HISTORY_FILE.exists():
        try:
            history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            history = []


def _save_history():
    HISTORY_FILE.write_text(
        json.dumps(history[-100:], ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _fit():
    docs = get_documents()
    summarizer.fit_collection([d["text"] for d in docs])


@app.on_event("startup")
def startup():
    _load_history()
    _fit()


def _result_to_dict(r, extra=None):
    d = {
        "title": r.title,
        "language": r.language,
        "source_id": r.source_id,
        "classical": r.classical,
        "keywords_flat": [{"term": t, "weight": round(w, 4)} for t, w in r.keywords_flat],
        "keywords_tree": r.keywords_tree,
        "topic_groups": r.topic_groups,
        "stats": r.stats,
        "sentence_scores": r.sentence_scores,
    }
    if extra:
        d.update(extra)
    return d


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    docs = get_documents()
    return templates.TemplateResponse(
        "index.html",
        context={"request": request, "active": "home", "docs": docs, "history_count": len(history)},
    )


@app.get("/doc/{doc_id}", response_class=HTMLResponse)
async def view_doc(request: Request, doc_id: str):
    doc = get_document(doc_id)
    if not doc:
        return templates.TemplateResponse(
            "index.html",
            context={"request": request, "active": "home", "docs": get_documents(), "error": "Документ не найден"},
        )
    return templates.TemplateResponse(
        "document.html",
        context={"request": request, "active": "home", "doc": doc},
    )


@app.get("/summarize/{doc_id}", response_class=HTMLResponse)
async def summarize_doc(request: Request, doc_id: str):
    doc = get_document(doc_id)
    if not doc:
        return templates.TemplateResponse(
            "index.html",
            context={"request": request, "active": "home", "docs": get_documents(), "error": "Документ не найден"},
        )
    result = summarizer.summarize(
        doc["text"], title=doc["title"], language=doc["language"], source_id=doc["id"]
    )
    payload = _result_to_dict(result, {"domain": doc.get("domain", "")})
    history.append(
        {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "source": doc["id"],
            "title": doc["title"],
            "language": doc["language"],
            "n_sent": len(result.classical),
            "n_kw": len(result.keywords_flat),
        }
    )
    _save_history()
    return templates.TemplateResponse(
        "result.html",
        context={
            "request": request,
            "active": "home",
            "doc": doc,
            "result": result,
            "payload": payload,
        },
    )


@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse(
        "upload.html",
        context={"request": request, "active": "upload"},
    )


@app.post("/upload", response_class=HTMLResponse)
async def upload_submit(
    request: Request,
    text: Optional[str] = Form(None),
    title: Optional[str] = Form("document"),
    language: Optional[str] = Form("unknown"),
    file: Optional[UploadFile] = File(None),
):
    content = ""
    src_name = title or "document"
    if file and file.filename:
        raw = await file.read()
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            content = raw.decode("latin-1", errors="replace")
        src_name = file.filename
    elif text and text.strip():
        content = text
    else:
        return templates.TemplateResponse(
            "upload.html",
            context={"request": request, "active": "upload", "error": "Введите текст или загрузите файл."},
        )

    result = summarizer.summarize(
        content, title=src_name, language=language or "unknown", source_id=src_name
    )
    history.append(
        {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "source": src_name,
            "title": src_name,
            "language": language,
            "n_sent": len(result.classical),
            "n_kw": len(result.keywords_flat),
        }
    )
    _save_history()
    doc = {
        "id": src_name,
        "title": src_name,
        "language": language,
        "domain": "",
        "text": content,
    }
    return templates.TemplateResponse(
        "result.html",
        context={"request": request, "active": "upload", "doc": doc, "result": result, "payload": _result_to_dict(result)},
    )


@app.get("/batch", response_class=HTMLResponse)
async def batch(request: Request):
    rows = []
    for doc in get_documents():
        r = summarizer.summarize(
            doc["text"], title=doc["title"], language=doc["language"], source_id=doc["id"]
        )
        rows.append(
            {
                "doc": doc,
                "n_sent": len(r.classical),
                "n_kw": len(r.keywords_flat),
                "top_kw": ", ".join(t for t, _ in r.keywords_flat[:5]),
                "first_sent": r.classical[0][:120] + "…" if r.classical else "",
            }
        )
    return templates.TemplateResponse(
        "batch.html",
        context={"request": request, "active": "batch", "rows": rows},
    )


@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    return templates.TemplateResponse(
        "history.html",
        context={"request": request, "active": "history", "history": list(reversed(history[-50:]))},
    )


@app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request):
    return templates.TemplateResponse(
        "help.html",
        context={"request": request, "active": "help"},
    )


@app.get("/export/{doc_id}")
async def export_doc(doc_id: str):
    doc = get_document(doc_id)
    if not doc:
        return {"error": "not found"}
    r = summarizer.summarize(
        doc["text"], title=doc["title"], language=doc["language"], source_id=doc["id"]
    )
    payload = _result_to_dict(r, {"domain": doc.get("domain", ""), "exported_at": datetime.now().isoformat()})
    data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    return StreamingResponse(
        io.BytesIO(data),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=summary_{doc_id}.json"},
    )


@app.get("/export_all")
async def export_all():
    items = []
    for doc in get_documents():
        r = summarizer.summarize(
            doc["text"], title=doc["title"], language=doc["language"], source_id=doc["id"]
        )
        items.append(_result_to_dict(r, {"domain": doc.get("domain", "")}))
    payload = {
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "documents": items,
        "history": history,
    }
    data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    return StreamingResponse(
        io.BytesIO(data),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=summaries_all.json"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)