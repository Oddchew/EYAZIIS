import time, requests

BASE = "http://127.0.0.1:8000"

text = "слово " * 10000
with open("test.txt", "w") as f:
    f.write(text)

r = requests.post(f"{BASE}/documents/upload",
                  files={"file": open("test.txt", "rb")})
doc_id = r.json()["id"]
print(f"Документ загружен, id={doc_id}\n")

cases = [
    {"query": "слово", "query_type": "lemma",     "limit": 50,  "label": "лемма, 50 результатов"},
    {"query": "слово", "query_type": "lemma",     "limit": 500, "label": "лемма, 500 результатов"},
    {"query": "слово", "query_type": "word_form", "limit": 50,  "label": "словоформа, 50 результатов"},
    {"query": "NOUN",  "query_type": "pos",        "limit": 50,  "label": "часть речи (NOUN), 50 результатов"},
    {"query": "слово", "query_type": "lemma",     "limit": 50,  "label": "лемма + фильтр по документу",
     "document_id": doc_id},
]

print(f"{'Тест':<40} {'Найдено':>8} {'Время API (мс)':>16} {'Время total (мс)':>18}")
print("-" * 85)

for case in cases:
    label = case.pop("label")
    
    start = time.time()
    r = requests.post(f"{BASE}/search",
                      json={"context_window": 5, **case})
    total_ms = round((time.time() - start) * 1000, 1)
    
    data = r.json()
    api_ms = data.get("execution_time_ms", "?")
    found  = data.get("total_found", "?")
    
    print(f"{label:<40} {str(found):>8} {str(api_ms):>16} {str(total_ms):>18}")
