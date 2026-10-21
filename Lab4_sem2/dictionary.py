# -*- coding: utf-8 -*-
"""Работа со словарём (SQLite)."""

import sqlite3
from config import DB_PATH

# Базовый словарь (медицина + искусство + частотные слова)
SEED_DICTIONARY = {
    # общие
    "the": ("", "DT"), "a": ("", "DT"), "an": ("", "DT"),
    "and": ("и", "CC"), "or": ("или", "CC"), "but": ("но", "CC"),
    "of": ("", "IN"), "in": ("в", "IN"), "on": ("на", "IN"), "at": ("в", "IN"),
    "to": ("к", "TO"), "for": ("для", "IN"), "with": ("с", "IN"), "by": ("", "IN"),
    "from": ("из", "IN"), "about": ("о", "IN"), "as": ("как", "IN"),
    "is": ("является", "VBZ"), "are": ("являются", "VBP"), "was": ("был", "VBD"),
    "were": ("были", "VBD"), "be": ("быть", "VB"), "been": ("был", "VBN"),
    "have": ("иметь", "VBP"), "has": ("имеет", "VBZ"), "had": ("имел", "VBD"),
    "do": ("делать", "VBP"), "does": ("делает", "VBZ"), "did": ("сделал", "VBD"),
    "can": ("может", "MD"), "may": ("может", "MD"), "must": ("должен", "MD"),
    "will": ("будет", "MD"), "should": ("следует", "MD"),
    "needs": ("нуждается в", "VBZ"), "need": ("нуждаться", "VB"),
    "carefully": ("тщательно", "RB"), "significantly": ("значительно", "RB"),
    "highly": ("весьма", "RB"), "deeply": ("глубоко", "RB"),
    "this": ("этот", "DT"), "that": ("тот", "DT"), "these": ("эти", "DT"), "those": ("те", "DT"),
    "it": ("оно", "PRP"), "he": ("он", "PRP"), "she": ("она", "PRP"), "they": ("они", "PRP"),
    "we": ("мы", "PRP"), "you": ("вы", "PRP"), "i": ("я", "PRP"),
    "his": ("его", "PRP$"), "her": ("её", "PRP$"), "their": ("их", "PRP$"), "its": ("его", "PRP$"),
    "not": ("не", "RB"), "no": ("нет", "DT"), "yes": ("да", "UH"),
    "very": ("очень", "RB"), "also": ("также", "RB"), "only": ("только", "RB"),
    "more": ("более", "RBR"), "most": ("наиболее", "RBS"),
    "which": ("который", "WDT"), "who": ("кто", "WP"), "what": ("что", "WP"),
    "when": ("когда", "WRB"), "where": ("где", "WRB"), "how": ("как", "WRB"),
    "than": ("чем", "IN"), "then": ("затем", "RB"), "so": ("так", "RB"),
    "if": ("если", "IN"), "because": ("потому что", "IN"),
    # медицина
    "patient": ("пациент", "NN"), "patients": ("пациенты", "NNS"),
    "doctor": ("врач", "NN"), "doctors": ("врачи", "NNS"),
    "physician": ("врач", "NN"), "surgeon": ("хирург", "NN"),
    "nurse": ("медсестра", "NN"), "hospital": ("больница", "NN"),
    "clinic": ("клиника", "NN"), "treatment": ("лечение", "NN"),
    "therapy": ("терапия", "NN"), "diagnosis": ("диагноз", "NN"),
    "disease": ("болезнь", "NN"), "illness": ("заболевание", "NN"),
    "symptom": ("симптом", "NN"), "symptoms": ("симптомы", "NNS"),
    "fever": ("лихорадка", "NN"), "pain": ("боль", "NN"),
    "infection": ("инфекция", "NN"), "inflammation": ("воспаление", "NN"),
    "virus": ("вирус", "NN"), "bacteria": ("бактерии", "NNS"),
    "blood": ("кровь", "NN"), "heart": ("сердце", "NN"),
    "lung": ("лёгкое", "NN"), "lungs": ("лёгкие", "NNS"),
    "brain": ("мозг", "NN"), "liver": ("печень", "NN"),
    "kidney": ("почка", "NN"), "kidneys": ("почки", "NNS"),
    "medicine": ("лекарство", "NN"), "drug": ("препарат", "NN"),
    "medication": ("медикамент", "NN"), "dose": ("доза", "NN"),
    "dosage": ("дозировка", "NN"), "side": ("побочный", "JJ"),
    "effect": ("эффект", "NN"), "effects": ("эффекты", "NNS"),
    "clinical": ("клинический", "JJ"), "medical": ("медицинский", "JJ"),
    "surgical": ("хирургический", "JJ"), "chronic": ("хронический", "JJ"),
    "acute": ("острый", "JJ"), "severe": ("тяжёлый", "JJ"),
    "mild": ("лёгкий", "JJ"), "positive": ("положительный", "JJ"),
    "negative": ("отрицательный", "JJ"), "normal": ("нормальный", "JJ"),
    "abnormal": ("патологический", "JJ"), "healthy": ("здоровый", "JJ"),
    "examine": ("обследовать", "VB"), "examined": ("обследовал", "VBD"),
    "diagnose": ("диагностировать", "VB"), "diagnosed": ("диагностировал", "VBD"),
    "treat": ("лечить", "VB"), "treated": ("лечил", "VBD"),
    "prescribe": ("назначить", "VB"), "prescribed": ("назначил", "VBD"),
    "recover": ("выздоравливать", "VB"), "recovered": ("выздоровел", "VBD"),
    "suffer": ("страдать", "VB"), "suffers": ("страдает", "VBZ"), "suffered": ("страдал", "VBD"),
    "cause": ("вызывать", "VB"), "causes": ("вызывает", "VBZ"), "caused": ("вызвал", "VBD"),
    "result": ("результат", "NN"), "results": ("результаты", "NNS"),
    "study": ("исследование", "NN"), "studies": ("исследования", "NNS"),
    "research": ("исследование", "NN"), "analysis": ("анализ", "NN"),
    "data": ("данные", "NNS"), "method": ("метод", "NN"), "methods": ("методы", "NNS"),
    "procedure": ("процедура", "NN"), "operation": ("операция", "NN"),
    "surgery": ("хирургия", "NN"), "intervention": ("вмешательство", "NN"),
    "risk": ("риск", "NN"), "risks": ("риски", "NNS"),
    "factor": ("фактор", "NN"), "factors": ("факторы", "NNS"),
    "condition": ("состояние", "NN"), "conditions": ("состояния", "NNS"),
    "health": ("здоровье", "NN"), "care": ("уход", "NN"),
    "prevention": ("профилактика", "NN"), "vaccine": ("вакцина", "NN"),
    "vaccination": ("вакцинация", "NN"), "antibody": ("антитело", "NN"),
    "immune": ("иммунный", "JJ"), "system": ("система", "NN"),
    "cell": ("клетка", "NN"), "cells": ("клетки", "NNS"),
    "tissue": ("ткань", "NN"), "organ": ("орган", "NN"), "organs": ("органы", "NNS"),
    "body": ("тело", "NN"), "temperature": ("температура", "NN"),
    "pressure": ("давление", "NN"), "pulse": ("пульс", "NN"), "rate": ("частота", "NN"),
    "high": ("высокий", "JJ"), "low": ("низкий", "JJ"),
    "increased": ("повышенный", "JJ"), "decreased": ("пониженный", "JJ"),
    "significant": ("значительный", "JJ"), "important": ("важный", "JJ"),
    "common": ("распространённый", "JJ"), "rare": ("редкий", "JJ"),
    "observed": ("наблюдаемый", "JJ"), "reported": ("сообщаемый", "JJ"),
    "showed": ("показал", "VBD"), "shows": ("показывает", "VBZ"),
    "found": ("обнаружил", "VBD"), "find": ("находить", "VB"),
    "include": ("включать", "VB"), "includes": ("включает", "VBZ"), "included": ("включал", "VBD"),
    "using": ("используя", "VBG"), "used": ("использовал", "VBD"), "use": ("использовать", "VB"),
    "based": ("основанный", "VBN"), "according": ("согласно", "VBG"),
    "during": ("во время", "IN"), "after": ("после", "IN"),
    "before": ("до", "IN"), "between": ("между", "IN"),
    "among": ("среди", "IN"), "through": ("через", "IN"),
    "into": ("в", "IN"), "over": ("над", "IN"), "under": ("под", "IN"),
    "without": ("без", "IN"), "against": ("против", "IN"),
    "such": ("такой", "JJ"), "other": ("другой", "JJ"),
    "same": ("тот же", "JJ"), "different": ("различный", "JJ"),
    "new": ("новый", "JJ"), "old": ("старый", "JJ"),
    "first": ("первый", "JJ"), "second": ("второй", "JJ"),
    "year": ("год", "NN"), "years": ("годы", "NNS"),
    "month": ("месяц", "NN"), "day": ("день", "NN"),
    "time": ("время", "NN"), "times": ("раз", "NNS"),
    "case": ("случай", "NN"), "cases": ("случаи", "NNS"),
    "group": ("группа", "NN"), "groups": ("группы", "NNS"),
    "level": ("уровень", "NN"), "levels": ("уровни", "NNS"),
    "value": ("значение", "NN"), "values": ("значения", "NNS"),
    "number": ("число", "NN"), "numbers": ("числа", "NNS"),
    "percent": ("процент", "NN"), "percentage": ("процент", "NN"),
    "age": ("возраст", "NN"), "sex": ("пол", "NN"),
    "male": ("мужской", "JJ"), "female": ("женский", "JJ"),
    "child": ("ребёнок", "NN"), "children": ("дети", "NNS"),
    "adult": ("взрослый", "NN"), "adults": ("взрослые", "NNS"),
    # искусство
    "art": ("искусство", "NN"), "artist": ("художник", "NN"), "artists": ("художники", "NNS"),
    "painting": ("картина", "NN"), "paintings": ("картины", "NNS"),
    "sculpture": ("скульптура", "NN"), "sculptures": ("скульптуры", "NNS"),
    "drawing": ("рисунок", "NN"), "canvas": ("холст", "NN"), "brush": ("кисть", "NN"),
    "color": ("цвет", "NN"), "colour": ("цвет", "NN"),
    "colors": ("цвета", "NNS"), "colours": ("цвета", "NNS"),
    "composition": ("композиция", "NN"), "style": ("стиль", "NN"),
    "technique": ("техника", "NN"), "techniques": ("техники", "NNS"),
    "masterpiece": ("шедевр", "NN"), "work": ("работа", "NN"), "works": ("работы", "NNS"),
    "exhibition": ("выставка", "NN"), "gallery": ("галерея", "NN"), "museum": ("музей", "NN"),
    "portrait": ("портрет", "NN"), "landscape": ("пейзаж", "NN"),
    "still": ("натюрморт", "JJ"), "life": ("жизнь", "NN"),
    "abstract": ("абстрактный", "JJ"), "realistic": ("реалистичный", "JJ"),
    "impressionist": ("импрессионистский", "JJ"), "modern": ("современный", "JJ"),
    "classical": ("классический", "JJ"), "contemporary": ("современный", "JJ"),
    "beautiful": ("красивый", "JJ"), "elegant": ("элегантный", "JJ"),
    "expressive": ("выразительный", "JJ"), "dramatic": ("драматичный", "JJ"),
    "subtle": ("тонкий", "JJ"), "bold": ("смелый", "JJ"),
    "vivid": ("яркий", "JJ"), "dark": ("тёмный", "JJ"), "light": ("светлый", "JJ"),
    "shadow": ("тень", "NN"), "form": ("форма", "NN"), "forms": ("формы", "NNS"),
    "line": ("линия", "NN"), "lines": ("линии", "NNS"),
    "shape": ("форма", "NN"), "shapes": ("формы", "NNS"),
    "texture": ("текстура", "NN"), "perspective": ("перспектива", "NN"),
    "harmony": ("гармония", "NN"), "balance": ("баланс", "NN"),
    "contrast": ("контраст", "NN"), "rhythm": ("ритм", "NN"),
    "emotion": ("эмоция", "NN"), "feeling": ("чувство", "NN"),
    "mood": ("настроение", "NN"), "atmosphere": ("атмосфера", "NN"),
    "critic": ("критик", "NN"), "criticism": ("критика", "NN"),
    "review": ("рецензия", "NN"), "interpretation": ("интерпретация", "NN"),
    "meaning": ("смысл", "NN"), "symbol": ("символ", "NN"), "symbolism": ("символизм", "NN"),
    "theme": ("тема", "NN"), "themes": ("темы", "NNS"),
    "subject": ("сюжет", "NN"), "subjects": ("сюжеты", "NNS"),
    "figure": ("фигура", "NN"), "figures": ("фигуры", "NNS"),
    "depicted": ("изображённый", "VBN"), "represents": ("представляет", "VBZ"),
    "expresses": ("выражает", "VBZ"), "conveys": ("передаёт", "VBZ"),
    "created": ("создал", "VBD"), "painted": ("написал", "VBD"),
    "sculpted": ("изваял", "VBD"), "exhibited": ("выставил", "VBD"),
    "famous": ("знаменитый", "JJ"), "renowned": ("известный", "JJ"),
    "talented": ("талантливый", "JJ"), "skilled": ("искусный", "JJ"),
    "innovative": ("инновационный", "JJ"), "traditional": ("традиционный", "JJ"),
    "unique": ("уникальный", "JJ"), "original": ("оригинальный", "JJ"),
    "influence": ("влияние", "NN"), "influenced": ("повлиял", "VBD"),
    "inspired": ("вдохновлённый", "VBN"), "inspiration": ("вдохновение", "NN"),
    "period": ("период", "NN"), "century": ("век", "NN"),
    "renaissance": ("ренессанс", "NN"), "baroque": ("барокко", "NN"),
    "impressionism": ("импрессионизм", "NN"), "expressionism": ("экспрессионизм", "NN"),
    "cubism": ("кубизм", "NN"), "surrealism": ("сюрреализм", "NN"),
    "oil": ("масло", "NN"), "watercolor": ("акварель", "NN"),
    "acrylic": ("акрил", "NN"), "charcoal": ("уголь", "NN"),
    "pastel": ("пастель", "NN"), "ink": ("тушь", "NN"),
    "marble": ("мрамор", "NN"), "bronze": ("бронза", "NN"),
    "wood": ("дерево", "NN"), "clay": ("глина", "NN"),
    "collection": ("коллекция", "NN"), "curator": ("куратор", "NN"),
    "viewer": ("зритель", "NN"), "audience": ("публика", "NN"), "public": ("публика", "NN"),
    "appreciation": ("оценка", "NN"), "aesthetic": ("эстетический", "JJ"),
    "beauty": ("красота", "NN"), "ugliness": ("уродство", "NN"),
    "mastery": ("мастерство", "NN"), "craftsmanship": ("мастерство", "NN"),
}


class DictionaryDB:
    """Простая обёртка над SQLite для словаря."""

    def __init__(self, path=DB_PATH):
        self.path = path
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._init_schema()
        self._seed_if_empty()

    def _init_schema(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS dictionary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                en_word TEXT NOT NULL COLLATE NOCASE,
                ru_word TEXT NOT NULL,
                pos_tag TEXT,
                frequency INTEGER DEFAULT 0,
                UNIQUE(en_word)
            )
        """)
        self.conn.commit()

    def _seed_if_empty(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM dictionary")
        if cur.fetchone()[0] == 0:
            for en, (ru, tag) in SEED_DICTIONARY.items():
                try:
                    cur.execute(
                        "INSERT OR IGNORE INTO dictionary (en_word, ru_word, pos_tag) VALUES (?, ?, ?)",
                        (en.lower(), ru, tag)
                    )
                except Exception:
                    pass
            self.conn.commit()

    def get_translation(self, word):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT ru_word, pos_tag FROM dictionary WHERE en_word = ? COLLATE NOCASE",
            (word.lower(),)
        )
        row = cur.fetchone()
        return row if row else (None, None)

    def add_or_update(self, en, ru, pos_tag=""):
        cur = self.conn.cursor()
        cur.execute(
            """INSERT INTO dictionary (en_word, ru_word, pos_tag)
               VALUES (?, ?, ?)
               ON CONFLICT(en_word) DO UPDATE SET
                   ru_word = excluded.ru_word,
                   pos_tag = excluded.pos_tag
            """,
            (en.lower().strip(), ru.strip(), pos_tag)
        )
        self.conn.commit()

    def delete(self, en):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM dictionary WHERE en_word = ? COLLATE NOCASE", (en.lower(),))
        self.conn.commit()

    def all_entries(self):
        cur = self.conn.cursor()
        cur.execute("SELECT en_word, ru_word, pos_tag, frequency FROM dictionary ORDER BY en_word")
        return cur.fetchall()

    def increment_freq(self, word):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE dictionary SET frequency = frequency + 1 WHERE en_word = ? COLLATE NOCASE",
            (word.lower(),)
        )

    def commit(self):
        self.conn.commit()

    def close(self):
        try:
            self.conn.commit()
        except Exception:
            pass
        self.conn.close()
