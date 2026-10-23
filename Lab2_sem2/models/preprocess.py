"""
Предварительная обработка текста и извлечение текста из HTML.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from typing import Optional


class _HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def extract_text_from_html(html: str) -> str:
    """Извлекает видимый текст из HTML-документа."""
    parser = _HTMLTextExtractor()
    try:
        parser.feed(html)
        parser.close()
    except Exception:
        # fallback: strip tags roughly
        return re.sub(r"<[^>]+>", " ", html)
    return " ".join(parser.parts)


def preprocess_text(text: str, keep_spaces: bool = True) -> str:
    """
    Нормализация текста для построения профилей:
    - lowercase
    - удаление цифр и большинства пунктуации
    - сохранение букв (включая диакритику) и пробелов
    """
    if not text:
        return ""
    text = text.lower()
    # keep letters (unicode) and spaces
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"_+", " ", text)
    text = re.sub(r"\s+", " " if keep_spaces else "", text)
    return text.strip()


def is_html_content(content: str) -> bool:
    """Грубая эвристика: выглядит ли строка как HTML."""
    sample = content[:2000].lower()
    return "<html" in sample or "<body" in sample or "<p>" in sample or "<div" in sample
