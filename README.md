# Corpus Manager

Корпусный менеджер для анализа текстов. Загрузка, морфологический анализ (pymorphy3), поиск по корпусу, конкордансы, статистика.

## Технологии

Python 3.11/3.12, FastAPI, SQLAlchemy, SQLite, pymorphy3

## Установка

1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. `python -m nltk.downloader punkt stopwords`
4. `python run.py`

API: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)