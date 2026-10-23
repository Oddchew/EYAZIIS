#!/usr/bin/env python3
"""
Лабораторная работа 2 — Автоматическое распознавание языка текста.
Вариант 7: Французский, Английский | HTML | N-грамм, алфавитный, нейросетевой.

Стек: FastAPI + Jinja2 + Uvicorn.
"""

from __future__ import annotations

import io
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from data.corpus import get_test_documents, get_training_corpus
from models.detector import LANG_DISPLAY, LanguageDetector, SUPPORTED_LANGUAGES
from models.preprocess import extract_text_from_html, is_html_content

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Определение языка текста",
    description="N-грамм, алфавитный, нейросетевой",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

detector = LanguageDetector(model_dir=DATA_DIR)

# История распознаваний (в памяти + JSON)
history: List[dict] = []
HISTORY_FILE = DATA_DIR / "history.json"


def _load_history():
    global history
    if HISTORY_FILE.exists():
        try:
            history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            history = []


def _save_history():
    HISTORY_FILE.write_text(
        json.dumps(history[-200:], ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _train_if_needed(force: bool = False):
    if detector.is_ready and not force:
        return detector.train_stats
    corpus = get_training_corpus()
    stats = detector.train(corpus, neural_epochs=70)
    return stats


@app.on_event("startup")
def startup():
    _load_history()
    _train_if_needed()


# --------------------------------------------------------------------------- routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "active": "home",
            "langs": SUPPORTED_LANGUAGES,
            "lang_display": LANG_DISPLAY,
            "ready": detector.is_ready,
            "train_stats": detector.train_stats,
            "history_count": len(history),
        },
    )


@app.get("/detect", response_class=HTMLResponse)
async def detect_page(request: Request):
    return templates.TemplateResponse(
        "detect.html",
        {
            "request": request,
            "active": "detect",
            "ready": detector.is_ready,
        },
    )


@app.post("/detect", response_class=HTMLResponse)
async def detect_submit(
    request: Request,
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    content = ""
    source_name = "pasted text"
    if file and file.filename:
        raw = await file.read()
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            content = raw.decode("latin-1", errors="replace")
        source_name = file.filename
        # save upload
        dest = UPLOAD_DIR / f"{int(time.time())}_{file.filename}"
        dest.write_bytes(raw)
    elif text and text.strip():
        content = text
    else:
        return templates.TemplateResponse(
            "detect.html",
            {
                "request": request,
                "active": "detect",
                "ready": detector.is_ready,
                "error": "Введите текст или загрузите HTML-файл.",
            },
        )

    if not detector.is_ready:
        _train_if_needed()

    results = detector.detect_all(content)
    vote = detector.majority_vote(results)
    plain = extract_text_from_html(content) if is_html_content(content) else content
    preview = plain[:400] + ("..." if len(plain) > 400 else "")

    entry = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "source": source_name,
        "preview": preview[:120],
        "vote": vote,
        "methods": {
            r.method: {
                "predicted": r.predicted,
                "scores": r.distances_or_probs,
                "ms": r.elapsed_ms,
            }
            for r in results
        },
    }
    history.append(entry)
    _save_history()

    return templates.TemplateResponse(
        "detect.html",
        {
            "request": request,
            "active": "detect",
            "ready": detector.is_ready,
            "results": results,
            "vote": vote,
            "vote_display": LANG_DISPLAY.get(vote, vote),
            "source_name": source_name,
            "preview": preview,
            "lang_display": LANG_DISPLAY,
            "content_len": len(plain),
        },
    )


@app.get("/batch", response_class=HTMLResponse)
async def batch_page(request: Request):
    """Тестирование на встроенной тестовой коллекции."""
    if not detector.is_ready:
        _train_if_needed()

    docs = get_test_documents()
    rows = []
    method_correct = {"N-грамм (Out-of-Place)": 0, "Алфавитный": 0, "Нейросетевой (MLP)": 0}
    method_time = {"N-грамм (Out-of-Place)": 0.0, "Алфавитный": 0.0, "Нейросетевой (MLP)": 0.0}
    vote_correct = 0

    for doc in docs:
        results = detector.detect_all(doc["html"])
        vote = detector.majority_vote(results)
        true_lang = doc["language"]
        ok_vote = vote == true_lang
        if ok_vote:
            vote_correct += 1
        row = {
            "id": doc["id"],
            "title": doc["title"],
            "true": true_lang,
            "vote": vote,
            "ok": ok_vote,
            "methods": {},
        }
        for r in results:
            correct = r.predicted == true_lang
            if correct:
                method_correct[r.method] += 1
            method_time[r.method] += r.elapsed_ms
            row["methods"][r.method] = {
                "pred": r.predicted,
                "ok": correct,
                "scores": r.distances_or_probs,
                "ms": r.elapsed_ms,
            }
        rows.append(row)

    n = len(docs) or 1
    summary = {
        "n": n,
        "vote_acc": round(100 * vote_correct / n, 1),
        "methods": {
            m: {
                "acc": round(100 * method_correct[m] / n, 1),
                "avg_ms": round(method_time[m] / n, 3),
            }
            for m in method_correct
        },
    }

    return templates.TemplateResponse(
        "batch.html",
        {
            "request": request,
            "active": "batch",
            "rows": rows,
            "summary": summary,
            "lang_display": LANG_DISPLAY,
        },
    )


@app.get("/train", response_class=HTMLResponse)
async def train_page(request: Request):
    return templates.TemplateResponse(
        "train.html",
        {
            "request": request,
            "active": "train",
            "stats": detector.train_stats,
            "ready": detector.is_ready,
        },
    )


@app.post("/train", response_class=HTMLResponse)
async def train_run(request: Request):
    stats = _train_if_needed(force=True)
    return templates.TemplateResponse(
        "train.html",
        {
            "request": request,
            "active": "train",
            "stats": stats,
            "ready": detector.is_ready,
            "message": "Модели успешно переобучены.",
        },
    )


@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    return templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "active": "history",
            "history": list(reversed(history[-100:])),
            "lang_display": LANG_DISPLAY,
        },
    )


@app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request):
    return templates.TemplateResponse(
        "help.html",
        {
            "request": request,
            "active": "help",
        },
    )


@app.get("/export")
async def export_results():
    """Сохранение сводной статистики и истории в JSON (скачивание)."""
    payload = {
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "variant": 7,
        "languages": SUPPORTED_LANGUAGES,
        "methods": ["N-грамм", "Алфавитный", "Нейросетевой"],
        "train_stats": detector.train_stats,
        "history": history,
    }
    data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    return StreamingResponse(
        io.BytesIO(data),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=lang_detect_results.json"},
    )


@app.get("/api/detect")
async def api_detect(text: str = ""):
    if not text.strip():
        return JSONResponse({"error": "empty text"}, status_code=400)
    if not detector.is_ready:
        _train_if_needed()
    results = detector.detect_all(text)
    vote = detector.majority_vote(results)
    return {
        "vote": vote,
        "methods": [
            {
                "method": r.method,
                "predicted": r.predicted,
                "scores": r.distances_or_probs,
                "elapsed_ms": r.elapsed_ms,
            }
            for r in results
        ],
    }


@app.get("/api/status")
async def api_status():
    return {
        "ready": detector.is_ready,
        "train_stats": detector.train_stats,
        "history_len": len(history),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=False)
