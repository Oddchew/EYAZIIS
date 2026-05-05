import time, requests

texts = {
    "5 слов": "слово " * 5,
    "50 слов": "слово " * 50,
    "500 слов": "слово " * 500,
    "5000 слов": "слово " * 5000,
    "50000 слов": "слово " * 50000,
    "500000 слов": "слово " * 500000,
}

for name, text in texts.items():
    with open("test.txt", "w") as f:
        f.write(text)
    
    start = time.time()
    r = requests.post("http://127.0.0.1:8000/documents/upload",
                      files={"file": open("test.txt", "rb")})
    elapsed = round((time.time() - start) * 1000)
    tokens = r.json().get("tokens_count", "?")
    print(f"{name}: {tokens} токенов, {elapsed} мс")
