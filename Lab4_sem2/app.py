# -*- coding: utf-8 -*-
"""
Веб-интерфейс системы машинного перевода.

Запуск:
    cd mt_web
    python app.py
Затем открыть http://127.0.0.1:5000
"""

import os
import io
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, send_file, jsonify
)

from config import SECRET_KEY, DB_PATH
from dictionary import DictionaryDB
from translator import MachineTranslator, POS_DECODE

app = Flask(__name__)
app.secret_key = SECRET_KEY

# один экземпляр БД и переводчика на процесс
db = DictionaryDB(DB_PATH)
translator = MachineTranslator(db)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        action = request.form.get("action", "translate")
        text = request.form.get("text", "").strip()

        if action == "example":
            examples = [
                "The patient has a severe fever and needs medical treatment. The doctor examined the clinical symptoms carefully.",
                "Clinical studies showed that the new therapy significantly reduced the risk of infection in adult patients.",
                "This painting is a beautiful masterpiece of modern art with vivid colors and elegant composition.",
                "The sculpture expresses deep emotion through bold forms and dramatic contrast of light and shadow.",
                "According to the research, chronic inflammation may cause abnormal cell growth and increase the risk of disease.",
            ]
            import random
            text = random.choice(examples)
            # просто подставляем пример, без перевода
            return render_template("index.html", text=text, result=None)

        if action == "clear":
            session.pop("last_result", None)
            return render_template("index.html", text="", result=None)

        if not text:
            flash("Введите текст на английском языке.", "warn")
            return render_template("index.html", text="", result=None)

        try:
            translation, total, translated, sorted_list, sentences = translator.translate_text(text)
            not_found = total - translated

            # данные для шаблона
            freq_rows = []
            for word, ru, pos, freq in sorted_list:
                freq_rows.append({
                    "word": word,
                    "ru": ru,
                    "pos": pos,
                    "pos_ru": POS_DECODE.get(pos, pos),
                    "freq": freq,
                })

            result = {
                "translation": translation,
                "total": total,
                "translated": translated,
                "not_found": not_found,
                "freq_rows": freq_rows,
                "sentences": sentences,
                "source": text,
            }
            # сохранение результата в сессии
            session["last_result"] = {
                "translation": translation,
                "total": total,
                "translated": translated,
                "not_found": not_found,
                "freq_rows": freq_rows,
                "sentences": sentences,
                "source": text,
            }
            flash(f"Переведено {translated} из {total} слов.", "ok")
        except Exception as e:
            flash(f"Ошибка при переводе: {e}", "error")
            result = None

    else:
        # восстановление последнего результата
        result = session.get("last_result")

    return render_template("index.html", text=result["source"] if result else "", result=result)


@app.route("/tree", methods=["POST"])
def build_tree():
    """AJAX: построить синтаксическое дерево для выбранного предложения."""
    sentence = request.form.get("sentence", "").strip()
    if not sentence:
        return jsonify({"ok": False, "tree": "", "msg": "Не выбрано предложение"})

    tree_str, msg = translator.build_parse_tree(sentence)
    return jsonify({
        "ok": True,
        "tree": tree_str or "",
        "msg": msg or "",
    })


@app.route("/download")
def download():
    """Скачать результаты в Unicode txt."""
    data = session.get("last_result")
    if not data:
        flash("Сначала выполните перевод.", "warn")
        return redirect(url_for("index"))

    buf = io.StringIO()
    buf.write("=== Результаты машинного перевода ===\n")
    buf.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    buf.write("Направление перевода: английский → русский\n\n")
    buf.write("--- Исходный текст ---\n")
    buf.write(data["source"] + "\n\n")
    buf.write("--- Перевод ---\n")
    buf.write(data["translation"] + "\n\n")
    buf.write("--- Статистика ---\n")
    buf.write(f"Слов: {data['total']}  |  Переведено: {data['translated']}  |  Не найдено: {data['not_found']}\n\n")
    buf.write("--- Частотный список слов (по убыванию частоты) ---\n")
    buf.write(f"{'Слово (EN)':<20} {'Перевод (RU)':<25} {'Тег':<8} {'Часть речи':<30} {'Частота':>8}\n")
    buf.write("-" * 95 + "\n")
    for row in data["freq_rows"]:
        buf.write(f"{row['word']:<20} {row['ru']:<25} {row['pos']:<8} {row['pos_ru']:<30} {row['freq']:>8}\n")

    mem = io.BytesIO(buf.getvalue().encode("utf-8"))
    mem.seek(0)
    filename = f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    return send_file(mem, as_attachment=True, download_name=filename, mimetype="text/plain; charset=utf-8")


@app.route("/dictionary", methods=["GET", "POST"])
def dictionary_page():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            en = request.form.get("en", "").strip()
            ru = request.form.get("ru", "").strip()
            pos = request.form.get("pos", "").strip()
            if en and ru is not None:
                db.add_or_update(en, ru, pos)
                flash(f"Добавлено: «{en}» → «{ru}»", "ok")
            else:
                flash("Нужно указать английское слово и перевод.", "warn")
        elif action == "edit":
            en = request.form.get("en", "").strip()
            ru = request.form.get("ru", "").strip()
            pos = request.form.get("pos", "").strip()
            if en:
                db.add_or_update(en, ru, pos)
                flash(f"Обновлено: «{en}»", "ok")
        elif action == "delete":
            en = request.form.get("en", "").strip()
            if en:
                db.delete(en)
                flash(f"Удалено: «{en}»", "ok")
        return redirect(url_for("dictionary_page"))

    entries = db.all_entries()
    return render_template("dictionary.html", entries=entries)


@app.teardown_appcontext
def shutdown(exception=None):
    pass  # БД живёт весь процесс


if __name__ == "__main__":
    # чтобы NLTK мог качать данные через прокси
    os.environ.setdefault("NLTK_ALLOW_PROXIED_URLOPEN", "1")
    print("Запуск сервера… открой http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
