import sys
import json
import pymorphy2

def analyze_word(word: str) -> dict:
    morph = pymorphy2.MorphAnalyzer(lang='ru')
    parsed = morph.parse(word)[0]
    return {
        'word_form': word,
        'lemma': parsed.normal_form,
        'pos': parsed.tag.POS,
        'grammemes': list(parsed.tag.grammemes),
        'score': parsed.score
    }

def main():
    # Ждем JSON-ввод из stdin
    input_line = sys.stdin.readline().strip()
    if not input_line:
        return

    request = json.loads(input_line)
    command = request.get('command')
    data = request.get('data')

    if command == 'analyze':
        word = data.get('word')
        result = analyze_word(word)
        print(json.dumps(result))
    elif command == 'bulk_analyze':
        words = data.get('words')
        results = [analyze_word(w) for w in words]
        print(json.dumps(results))
    else:
        print(json.dumps({"error": "Unknown command"}))

if __name__ == "__main__":
    main()