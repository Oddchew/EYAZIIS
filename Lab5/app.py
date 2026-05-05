from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import re
import json
import datetime
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# --- NLTK data download ---
for pkg in ['punkt', 'punkt_tab', 'stopwords']:
    nltk.download(pkg, quiet=True)

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = os.getenv("API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("API_KEY не найден в .env файле!")

HISTORY_FILE = "chat_history.json"

gemini_contexts: dict[str, list] = {}  

try:
    RUSSIAN_STOPWORDS = set(stopwords.words('russian'))
except LookupError:
    RUSSIAN_STOPWORDS = set()

GREETING_WORDS = {
    'здравствуйте', 'здравствуй', 'приветствую', 'салют',
    'добрый день', 'доброе утро', 'добрый вечер',
    'добрый', 'доброе', 'доброго', 'здравия желаю', 'здравия',
    
    'привет', 'здарова', 'дарова', 'здорово', 'здорова', 'здаров',
    'здрасьте', 'здрасте', 'ку', 'куку', 'хай', 'хэй', 'хайя',
    'хелло', 'хеллоу', 'йо', 'йоу',
    
    'приветик', 'приветочки', 'приветос', 'здаровчик',
    'хэйло', 'лол нет' 
}

HELP_WORDS = {
    'помощь', 'помоги', 'помогите', 'справка', 'подсказка',
    'поддержка', 'консультация', 'инструкция', 'руководство',
    'гайд', 'мануал', 'FAQ', 'фак', 'документация', 'документация',
    
    'умеешь', 'можешь', 'команды', 'функции', 'возможности',
    'навыки', 'фичи', 'опции', 'модули', 'что умеешь', 'что можешь',
    'как работать', 'как пользоваться', 'как начать', 'с чего начать',
    
    'хелп', 'хэлп', 'подскажи', 'объясни', 'покажи', 'расскажи', 'научи',
    'помоги пж', 'плиз', 'плз', 'что делать', 'куда жать', 'как спросить',
    'че умеешь', 'чё умеешь', 'что ты можешь', 'как тебя юзать', 'как включить'
}
TRANSPORT_KEYWORDS = {
    'машина', 'автомобиль', 'авто', 'автобус', 'поезд', 'самолет', 'самолёт',
    'корабль', 'метро', 'трамвай', 'троллейбус', 'велосипед', 'мотоцикл',
    'грузовик', 'транспорт', 'дорога', 'движение', 'перевозка', 'двигатель',
    'топливо', 'электромобиль', 'скоростной', 'железнодорожный', 'авиация',
    'флот', 'пдд', 'правила', 'водитель', 'пилот', 'машинист', 'капитан',
    'шоссе', 'магистраль', 'аэропорт', 'вокзал', 'порт', 'судно', 'яхта',
    'ракета', 'вертолет', 'вертолёт', 'дрон', 'скутер', 'такси', 'каршеринг',
    'маршрут', 'рейс', 'билет', 'расписание', 'бензин', 'дизель', 'гибрид',
    'газ', 'электрический', 'колесо', 'тормоз', 'руль', 'подвеска', 'кпп',
    'трансмиссия', 'кузов', 'крыло', 'фары', 'шины', 'мост', 'тоннель',
}

HELP_TEXT = """🚌 <strong>Транспортный Помощник — Справка</strong>

<strong>Что я умею:</strong>
<ul>
  <li>🚗 <strong>Виды транспорта</strong> — автомобили, поезда, самолёты, корабли, общественный транспорт</li>
  <li>🔧 <strong>Устройство и технологии</strong> — двигатели, трансмиссии, топливные системы, электрика</li>
  <li>📜 <strong>История транспорта</strong> — от первых повозок до современных электромобилей и гиперлупов</li>
  <li>📋 <strong>ПДД и безопасность</strong> — правила дорожного движения, знаки, штрафы</li>
  <li>🏗️ <strong>Инфраструктура</strong> — дороги, аэропорты, железные дороги, порты, развязки</li>
  <li>🌍 <strong>Экология транспорта</strong> — выбросы, альтернативное топливо, электромобили</li>
</ul>

<strong>Примеры вопросов:</strong>
<ul>
  <li>«Как работает двигатель внутреннего сгорания?»</li>
  <li>«Чем отличается ABS от ESP?»</li>
  <li>«История появления метро в Москве»</li>
  <li>«Какие знаки запрещают обгон?»</li>
  <li>«Расскажи о технологии Hyperloop»</li>
</ul>

<strong>Управление историей:</strong>
<ul>
  <li>Нажмите <strong>«Новый чат»</strong> — для начала новой беседы</li>
  <li>Наведите курсор на сообщение — для редактирования его текста</li>
</ul>"""


def preprocess(text: str) -> tuple[list[str], list[str]]:
    """Tokenise text and remove stopwords; returns (raw_tokens, filtered_tokens)."""
    try:
        tokens = word_tokenize(text.lower(), language='russian')
    except Exception:
        tokens = text.lower().split()
    alpha = [t for t in tokens if t.isalpha()]
    filtered = [t for t in alpha if t not in RUSSIAN_STOPWORDS]
    return alpha, filtered


def detect_intent(tokens: list[str]) -> str:
    token_set = set(tokens)
    if token_set & GREETING_WORDS:
        return 'greeting'
    if token_set & HELP_WORDS:
        return 'help'
    if token_set & TRANSPORT_KEYWORDS:
        return 'transport'
    return 'general'


# ─────────────────────────────────────────────
#  Markdown → HTML
# ─────────────────────────────────────────────
def md_to_html(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$',  r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$',   r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'^---$', '<hr>', text, flags=re.MULTILINE)

    def replace_list(m):
        items = re.findall(r'\n[*-] (.+)', m.group(1))
        return '<ul>' + ''.join(f'<li>{i.strip()}</li>' for i in items) + '</ul>'

    text = re.sub(r'(\n[*-] .+\n(?:[*-] .+\n?)*)', replace_list, text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.*?)__',     r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'(?<!_)_(?!_)(.+?)(?<!_)_(?!_)',       r'<em>\1</em>', text)
    text = text.replace('\n\n', '</p><p>').replace('\n', '<br>')
    text = '<p>' + text + '</p>'
    text = text.replace('<p></p>', '')
    return text


# ─────────────────────────────────────────────
#  Persistent history helpers
# ─────────────────────────────────────────────
def load_all_sessions() -> dict:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def persist(data: dict) -> None:
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def record_exchange(session_id: str, user_msg: str, bot_reply: str, ts: str) -> None:
    data = load_all_sessions()
    if session_id not in data:
        title = user_msg[:40] + ('…' if len(user_msg) > 40 else '')
        data[session_id] = {'created': ts, 'title': title, 'messages': []}
    data[session_id]['messages'].extend([
        {'role': 'user',      'content': user_msg,  'timestamp': ts},
        {'role': 'assistant', 'content': bot_reply, 'timestamp': ts},
    ])
    persist(data)


def render_session_for_frontend(session_data: dict) -> dict:
    """Return a copy of session data with bot messages converted to HTML."""
    rendered = {**session_data, 'messages': []}
    for msg in session_data.get('messages', []):
        if msg.get('role') == 'assistant':
            # Convert markdown to HTML for bot replies
            rendered['messages'].append({
                **msg,
                'content': md_to_html(msg['content'])
            })
        else:
            rendered['messages'].append(msg)
    return rendered


# ─────────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    body        = request.json or {}
    user_msg    = (body.get('message') or '').strip()
    session_id  = body.get('session_id') or 'default'

    if not user_msg:
        return jsonify({'error': 'Сообщение не может быть пустым'}), 400

    ts = datetime.datetime.now().isoformat()

    # ── NLP preprocessing ──────────────────────
    tokens, filtered = preprocess(user_msg)
    intent = detect_intent(tokens)

    # ── Short-circuit: greeting ─────────────────
    if intent == 'greeting' and len(tokens) <= 4:
        reply_raw  = 'Привет! Я транспортный помощник. Задайте мне вопрос о любом виде транспорта, ПДД, истории или инфраструктуре.'
        reply_html = f'<p>{reply_raw}</p>'
        record_exchange(session_id, user_msg, reply_raw, ts)
        return jsonify({'reply': reply_html, 'intent': intent})

    # ── Short-circuit: help ─────────────────────
    if intent == 'help' and len(filtered) <= 3:
        record_exchange(session_id, user_msg, '[справка]', ts)
        return jsonify({'reply': HELP_TEXT, 'intent': 'help'})

    # ── Call Gemini with multi-turn context ─────
    try:
        client = genai.Client(
            api_key=GOOGLE_API_KEY,
            http_options=types.HttpOptions(api_version='v1beta'),
        )

        system_prompt = (
            "Ты — дружелюбный и компетентный помощник-эксперт в области транспорта. "
            "Отвечай только на вопросы, связанные с видами транспорта, их устройством, "
            "историей, технологиями, правилами дорожного движения и транспортной "
            "инфраструктурой. Если вопрос не относится к транспорту — вежливо откажись. "
            "Отвечай на русском языке. Используй Markdown для форматирования."
        )

        # Maintain rolling context (last 10 turns)
        ctx = gemini_contexts.setdefault(session_id, [])
        ctx.append({'role': 'user', 'parts': [{'text': user_msg}]})
        contents = ctx[-10:]

        config = types.GenerateContentConfig(system_instruction=system_prompt)
        response = client.models.generate_content(
            model='gemma-4-31b-it',
            contents=contents,
            config=config,
        )

        model_text = response.text
        ctx.append({'role': 'model', 'parts': [{'text': model_text}]})

        record_exchange(session_id, user_msg, model_text, ts)
        return jsonify({'reply': md_to_html(model_text), 'intent': intent})

    except Exception as exc:
        print(f'[ERROR] Gemini: {exc}')
        return jsonify({'error': f'Ошибка при обращении к модели: {exc}'}), 500


# ── Session management endpoints ──────────────
@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    data = load_all_sessions()
    summary = {
        sid: {
            'created':       s['created'],
            'title':         s['title'],
            'message_count': len(s['messages']),
        }
        for sid, s in data.items()
    }
    return jsonify(summary)


@app.route('/api/sessions/new', methods=['POST'])
def new_session():
    session_id = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    gemini_contexts[session_id] = []
    return jsonify({'session_id': session_id})


@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    data = load_all_sessions()
    if session_id not in data:
        return jsonify({'error': 'Сессия не найдена'}), 404
    
    # Render bot messages as HTML before sending to frontend
    session = render_session_for_frontend(data[session_id])
    return jsonify(session)


@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    data = load_all_sessions()
    if session_id in data:
        del data[session_id]
        persist(data)
    gemini_contexts.pop(session_id, None)
    return jsonify({'success': True})


@app.route('/api/sessions/<session_id>/messages/<int:idx>', methods=['PUT'])
def edit_message(session_id, idx):
    body        = request.json or {}
    new_content = (body.get('content') or '').strip()
    if not new_content:
        return jsonify({'error': 'Содержимое не может быть пустым'}), 400

    data = load_all_sessions()
    if session_id not in data:
        return jsonify({'error': 'Сессия не найдена'}), 404
    msgs = data[session_id]['messages']
    if idx >= len(msgs):
        return jsonify({'error': 'Сообщение не найдено'}), 404

    msgs[idx]['content'] = new_content
    msgs[idx]['edited']  = True
    persist(data)
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)