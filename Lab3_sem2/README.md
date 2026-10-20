# Автоматическое реферирование документов

Вариант 7: английский / французский; computer science + литература.

## Методы

1. **Классический реферат** — sentence extraction по формулам методички (Posd, Posp, модифицированный TF·IDF).
2. **Ключевые слова** — список и иерархия (корень → составные термины).
3. **Тематические группы** — группировка предложений по ключевым терминам (вместо OSTIS).

## Запуск

```bash
pip install -r requirements.txt
python app.py
# http://localhost:8000
```

## Структура

```
app.py
models/preprocess.py
models/summarizer.py
data/collection.py
templates/
static/style.css
```
