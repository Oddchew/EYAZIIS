#!/usr/bin/env python3
"""
Веб-интерфейс ИПС (Boolean).
Элемент ИИ: интерфейс с пользователем.
Документы хранятся в SQLite (+ JSON-бэкап).
"""

import os
from datetime import date

from flask import (
    Flask, request, render_template, redirect, url_for, jsonify, flash,
)

from models.index import InvertedIndex
from models.search import BooleanSearchEngine
from models.metrics import MetricsEvaluator
from models.storage import DocumentStore, DEFAULT_JSON
from models.interface_ai import (
    suggest_terms, highlight_snippet, related_terms, query_hints,
)
from data.collection import RELEVANCE_JUDGMENTS

app = Flask(__name__)
app.secret_key = "ips-lab-secret"

store = DocumentStore()
index = InvertedIndex()
engine = None
evaluator = MetricsEvaluator(RELEVANCE_JUDGMENTS)


def rebuild_index():
    global index, engine
    index = InvertedIndex()
    docs = store.get_all()
    index.build_from_dict(docs)
    engine = BooleanSearchEngine(index)
    store.export_json()  # актуальный JSON-снимок
    return len(docs)


rebuild_index()


@app.route("/")
def search():
    query = request.args.get("q", "").strip()
    results = []
    related = []
    if query:
        raw = engine.search(query)
        for r in raw:
            doc = index.documents[r["documentId"]]
            r["snippet_html"] = highlight_snippet(doc.text, r["matched_terms"])
            results.append(r)
        related = related_terms(index, query)

    return render_template(
        "search.html",
        active="search",
        query=query,
        results=results,
        related=related,
        hints=query_hints(index),
        doc_count=index.N,
    )


@app.route("/api/suggest")
def api_suggest():
    q = request.args.get("q", "").strip()
    return jsonify(suggest_terms(index, q))


@app.route("/metrics")
def metrics_page():
    metrics = evaluator.evaluate_all(engine)
    n = len(metrics) or 1
    avg_p = sum(m["precision"] for m in metrics) / n
    avg_r = sum(m["recall"] for m in metrics) / n
    avg_f = sum(m["f_measure"] for m in metrics) / n
    avg_ap = sum(m["average_precision"] for m in metrics) / n
    labels = [
        (m["query"][:28] + "…" if len(m["query"]) > 28 else m["query"])
        for m in metrics
    ]
    return render_template(
        "metrics.html",
        active="metrics",
        metrics=metrics,
        avg_p=avg_p, avg_r=avg_r, avg_f=avg_f, avg_ap=avg_ap,
        labels=labels,
        precision_vals=[m["precision"] for m in metrics],
        recall_vals=[m["recall"] for m in metrics],
        f1_vals=[m["f_measure"] for m in metrics],
    )


@app.route("/docs")
def docs_page():
    return render_template(
        "docs.html",
        active="docs",
        docs=store.get_all(),
    )


@app.route("/doc/<int:doc_id>")
def doc_detail(doc_id):
    doc = index.documents.get(doc_id)
    if not doc:
        return redirect(url_for("docs_page"))
    term_weights = []
    for term, tf in sorted(doc.term_freq.items(), key=lambda x: -x[1]):
        idf = index.idf(term)
        term_weights.append({
            "term": term, "tf": tf, "idf": idf, "weight": tf * idf,
        })
    return render_template(
        "doc_detail.html", active="docs", doc=doc, term_weights=term_weights,
    )


@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    message = None
    error = None

    if request.method == "POST":
        action = request.form.get("action", "add")

        if action == "add_text":
            title = request.form.get("title", "").strip()
            text = request.form.get("text", "").strip()
            if not title or not text:
                error = "Укажите заголовок и текст"
            else:
                doc_id = store.add(title, text, date.today().isoformat())
                rebuild_index()
                message = f"Документ [{doc_id}] «{title}» добавлен. В индексе: {index.N}"

        elif action == "add_file":
            f = request.files.get("file")
            if not f or not f.filename:
                error = "Выберите файл"
            else:
                try:
                    raw = f.read()
                    try:
                        content = raw.decode("utf-8")
                    except UnicodeDecodeError:
                        content = raw.decode("latin-1")
                    title = request.form.get("title", "").strip() or os.path.splitext(f.filename)[0]
                    doc_id = store.add(title, content, date.today().isoformat())
                    rebuild_index()
                    message = f"Файл загружен как [{doc_id}] «{title}». В индексе: {index.N}"
                except Exception as e:
                    error = f"Ошибка чтения файла: {e}"

        elif action == "import_json":
            f = request.files.get("json_file")
            if not f or not f.filename:
                error = "Выберите JSON-файл"
            else:
                try:
                    path = DEFAULT_JSON
                    f.save(path)
                    n = store.import_json(path, clear=False)
                    rebuild_index()
                    message = f"Импортировано из JSON. Документов в базе: {store.count()}"
                except Exception as e:
                    error = f"Ошибка импорта: {e}"

        elif action == "delete":
            try:
                doc_id = int(request.form.get("doc_id", 0))
            except ValueError:
                doc_id = 0
            if store.delete(doc_id):
                rebuild_index()
                message = f"Документ [{doc_id}] удалён. В индексе: {index.N}"
            else:
                error = f"Документ [{doc_id}] не найден"

    return render_template(
        "upload.html",
        active="upload",
        message=message,
        error=error,
        docs=store.get_all(),
        doc_count=index.N,
    )


@app.route("/help")
def help_page():
    return render_template("help.html", active="help")


if __name__ == "__main__":
    print(f"документов в БД: {store.count()}")
    print("http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
