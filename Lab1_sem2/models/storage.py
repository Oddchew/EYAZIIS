"""Хранение документов в SQLite + выгрузка/загрузка JSON."""

import json
import os
import sqlite3
from typing import Dict, List, Optional

from models.document import Document

DEFAULT_DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "documents.db")
DEFAULT_JSON = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "documents.json")


class DocumentStore:
    def __init__(self, db_path: str = DEFAULT_DB):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    text TEXT NOT NULL,
                    date TEXT DEFAULT '2026-01-01'
                )
            """)
            conn.commit()

    def count(self) -> int:
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS n FROM documents").fetchone()
            return row["n"]

    def is_empty(self) -> bool:
        return self.count() == 0

    def get_all(self) -> Dict[int, dict]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, title, text, date FROM documents ORDER BY id"
            ).fetchall()
        return {
            r["id"]: {"title": r["title"], "text": r["text"], "date": r["date"]}
            for r in rows
        }

    def get(self, doc_id: int) -> Optional[dict]:
        with self._connect() as conn:
            r = conn.execute(
                "SELECT id, title, text, date FROM documents WHERE id = ?",
                (doc_id,),
            ).fetchone()
        if not r:
            return None
        return {"id": r["id"], "title": r["title"], "text": r["text"], "date": r["date"]}

    def next_id(self) -> int:
        with self._connect() as conn:
            row = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 AS n FROM documents").fetchone()
            return row["n"]

    def add(self, title: str, text: str, date: str = "", doc_id: Optional[int] = None) -> int:
        if doc_id is None:
            doc_id = self.next_id()
        if not date:
            from datetime import date as dt
            date = dt.today().isoformat()
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO documents (id, title, text, date) VALUES (?, ?, ?, ?)",
                (doc_id, title.strip(), text.strip(), date),
            )
            conn.commit()
        return doc_id

    def delete(self, doc_id: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
            conn.commit()
            return cur.rowcount > 0

    def load_from_dict(self, docs: Dict[int, dict], clear: bool = True):
        with self._connect() as conn:
            if clear:
                conn.execute("DELETE FROM documents")
            for doc_id, data in docs.items():
                conn.execute(
                    "INSERT OR REPLACE INTO documents (id, title, text, date) VALUES (?, ?, ?, ?)",
                    (
                        int(doc_id),
                        data["title"],
                        data["text"],
                        data.get("date", "2026-01-01"),
                    ),
                )
            conn.commit()

    def export_json(self, path: str = DEFAULT_JSON):
        data = {str(k): v for k, v in self.get_all().items()}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def import_json(self, path: str = DEFAULT_JSON, clear: bool = True):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        docs = {int(k): v for k, v in data.items()}
        self.load_from_dict(docs, clear=clear)
        return len(docs)
