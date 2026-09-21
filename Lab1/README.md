# ИПС — Boolean search (вариант 7)

## Структура

```
app.py              — веб-интерфейс (Flask)
console.py          — консольный режим
models/
  document.py       — Document, токенизация, стоп-слова
  index.py          — инвертированный индекс, idf, веса (1.5)–(1.6)
  search.py         — Boolean-поиск (AND/OR/NOT)
  metrics.py        — метрики ROMIP
data/
  collection.py     — коллекция документов + qrels
templates/          — HTML-шаблоны
static/style.css    — стили
```

## Запуск

```bash
# веб
python3 app.py
# http://localhost:5000  (или http://<IP>:5000 из локальной сети)

# консоль
python3 console.py
```

## Возможности

- Boolean-поиск (AND, OR, NOT)
- Активные ссылки на документы
- Список слов запроса, присутствующих в документе
- Веса терминов по формулам (1.5)–(1.6)
- Метрики ROMIP: P, R, F1, P@5, P@10, AP, R-Precision
- Графики метрик (Chart.js)
- Справка
