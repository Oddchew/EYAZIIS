# -*- coding: utf-8 -*-
"""Переводчик и синтаксический разбор."""

import re
from collections import Counter, defaultdict

import nltk
from nltk import pos_tag, word_tokenize, sent_tokenize
from nltk.tree import Tree
from nltk import CFG, ChartParser

from dictionary import DictionaryDB

# Расшифровка тегов Penn Treebank
POS_DECODE = {
    "CC": "сочинительный союз",
    "CD": "числительное",
    "DT": "артикль / определитель",
    "EX": "there (экзистенциальное)",
    "FW": "иностранное слово",
    "IN": "предлог / подчинительный союз",
    "JJ": "прилагательное",
    "JJR": "прилагательное (сравнительная степень)",
    "JJS": "прилагательное (превосходная степень)",
    "LS": "маркер списка",
    "MD": "модальный глагол",
    "NN": "существительное (ед. число)",
    "NNS": "существительное (мн. число)",
    "NNP": "имя собственное (ед.)",
    "NNPS": "имя собственное (мн.)",
    "PDT": "предетерминатор",
    "POS": "притяжательное окончание",
    "PRP": "личное местоимение",
    "PRP$": "притяжательное местоимение",
    "RB": "наречие",
    "RBR": "наречие (сравнительная)",
    "RBS": "наречие (превосходная)",
    "RP": "частица",
    "SYM": "символ",
    "TO": "to (инфинитив)",
    "UH": "междометие",
    "VB": "глагол (базовая форма)",
    "VBD": "глагол (прошедшее время)",
    "VBG": "глагол (герундий / причастие наст.)",
    "VBN": "глагол (причастие прош.)",
    "VBP": "глагол (наст. вр., не 3л. ед.)",
    "VBZ": "глагол (наст. вр., 3л. ед.)",
    "WDT": "вопросительный определитель",
    "WP": "вопросительное местоимение",
    "WP$": "вопросительное притяжательное",
    "WRB": "вопросительное наречие",
    ".": "знак препинания",
    ",": "запятая",
    ":": "двоеточие / точка с запятой",
    "''": "кавычки",
    "``": "кавычки",
    "(": "скобка",
    ")": "скобка",
}

BASE_GRAMMAR_STR = """
S -> NP VP | NP VP PP
NP -> DT NN | DT JJ NN | DT NN NN | JJ NN | NN | NNS | DT NNS | PRP | DT JJ NNS
VP -> VBZ NP | VBD NP | VBZ NP PP | VBD NP PP | VB NP | VBP NP | MD VP | VBZ ADJP | VBD ADJP
PP -> IN NP
ADJP -> JJ | RB JJ
DT -> "the" | "a" | "an" | "The" | "A" | "An" | "this" | "that" | "these" | "those"
NN -> "patient" | "doctor" | "fever" | "treatment" | "disease" | "symptom" | "pain" | "infection"
NN -> "art" | "artist" | "painting" | "sculpture" | "color" | "style" | "work" | "composition"
NN -> "hospital" | "clinic" | "medicine" | "diagnosis" | "therapy" | "result" | "study"
NN -> "heart" | "blood" | "brain" | "cell" | "system" | "body" | "condition"
NN -> "masterpiece" | "gallery" | "museum" | "portrait" | "landscape" | "technique"
NNS -> "patients" | "doctors" | "symptoms" | "effects" | "results" | "studies" | "methods"
NNS -> "artists" | "paintings" | "sculptures" | "colors" | "works" | "figures"
JJ -> "severe" | "mild" | "clinical" | "medical" | "chronic" | "acute" | "high" | "low"
JJ -> "beautiful" | "elegant" | "expressive" | "modern" | "classical" | "abstract" | "vivid"
JJ -> "significant" | "important" | "common" | "rare" | "new" | "old" | "positive" | "negative"
VBZ -> "has" | "is" | "shows" | "includes" | "causes" | "represents" | "expresses" | "conveys"
VBD -> "examined" | "diagnosed" | "treated" | "found" | "showed" | "painted" | "created" | "exhibited"
VBP -> "have" | "are" | "show" | "include"
VB -> "be" | "have" | "treat" | "examine" | "diagnose" | "create" | "paint"
MD -> "can" | "may" | "must" | "will" | "should"
IN -> "with" | "of" | "in" | "on" | "for" | "by" | "from" | "about" | "during" | "after" | "before"
RB -> "very" | "also" | "only" | "carefully" | "significantly" | "highly"
PRP -> "it" | "he" | "she" | "they" | "we" | "you"
"""


def ensure_nltk_data():
    """Подтянуть необходимые данные NLTK при первом запуске."""
    for resource in (
        "tokenizers/punkt",
        "tokenizers/punkt_tab",
        "taggers/averaged_perceptron_tagger_eng",
        "taggers/averaged_perceptron_tagger",
    ):
        try:
            nltk.data.find(resource)
        except LookupError:
            name = resource.split("/")[-1]
            nltk.download(name, quiet=True)


class MachineTranslator:
    """Словарный переводчик + морфология NLTK + простой CFG-парсер."""

    def __init__(self, db: DictionaryDB):
        self.db = db
        ensure_nltk_data()

    def translate_word(self, word, pos=None):
        pure = re.sub(r"[^\w'-]", "", word)
        punct = word[len(pure):] if pure else word
        if not pure:
            return word, False

        ru, tag = self.db.get_translation(pure)
        if ru is not None:
            self.db.increment_freq(pure)
            # пустой перевод (артикли the/a/an) — просто пропускаем слово
            if ru == "":
                return "", True
            return ru + punct, True
        return word, False

    def translate_text(self, text):
        if not text.strip():
            return "", 0, 0, [], []

        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)

        translated_tokens = []
        translated_count = 0
        word_info = []

        for token, pos in tagged:
            ru, ok = self.translate_word(token, pos)
            if ok:
                translated_count += 1
                # ru может быть "" (артикли) — так и оставляем
                translated_tokens.append(ru)
            else:
                translated_tokens.append(token)
            if re.match(r"[\w'-]+", token):
                word_info.append((token.lower(), ru if ok else "—", pos, 1))

        freq = Counter(t.lower() for t in tokens if re.match(r"[\w'-]+", t))
        unique_info = {}
        for orig, ru, pos, _ in word_info:
            if orig not in unique_info:
                unique_info[orig] = (ru, pos, freq[orig])
            else:
                unique_info[orig] = (unique_info[orig][0], unique_info[orig][1], freq[orig])

        sorted_list = sorted(
            [(w, info[0], info[1], info[2]) for w, info in unique_info.items()],
            key=lambda x: (-x[3], x[0])
        )

        translation = " ".join(t for t in translated_tokens if t)
        translation = re.sub(r"\s+([.,;:!?])", r"\1", translation)
        translation = re.sub(r"\s+", " ", translation).strip()

        total_words = sum(1 for t in tokens if re.match(r"[\w'-]+", t))
        sentences = sent_tokenize(text)
        self.db.commit()
        return translation, total_words, translated_count, sorted_list, sentences

    def build_parse_tree(self, sentence):
        tokens = word_tokenize(sentence)
        clean = [t for t in tokens if re.match(r"[\w'-]+", t)]
        if not clean:
            return None, "Пустое предложение"

        grammar_str = BASE_GRAMMAR_STR
        tagged = pos_tag(clean)
        extra_rules = defaultdict(set)
        for w, tag in tagged:
            if tag.startswith("NN"):
                extra_rules["NN" if tag == "NN" else "NNS"].add(f'"{w}"')
            elif tag.startswith("JJ"):
                extra_rules["JJ"].add(f'"{w}"')
            elif tag.startswith("VB"):
                if tag == "VBZ":
                    extra_rules["VBZ"].add(f'"{w}"')
                elif tag == "VBD":
                    extra_rules["VBD"].add(f'"{w}"')
                elif tag == "VBP":
                    extra_rules["VBP"].add(f'"{w}"')
                else:
                    extra_rules["VB"].add(f'"{w}"')
            elif tag == "IN":
                extra_rules["IN"].add(f'"{w}"')
            elif tag == "RB":
                extra_rules["RB"].add(f'"{w}"')
            elif tag == "DT":
                extra_rules["DT"].add(f'"{w}"')
            elif tag == "PRP":
                extra_rules["PRP"].add(f'"{w}"')
            elif tag == "MD":
                extra_rules["MD"].add(f'"{w}"')

        for nonterm, terminals in extra_rules.items():
            if terminals:
                grammar_str += f'\n{nonterm} -> {" | ".join(sorted(terminals))}'

        try:
            grammar = CFG.fromstring(grammar_str)
            parser = ChartParser(grammar)
            trees = list(parser.parse(clean))
            if trees:
                return trees[0].pformat(margin=80), None
            return self._fallback_tree(tagged), "Полный разбор не удался — показано приближённое дерево по частям речи"
        except Exception as e:
            return self._fallback_tree(tagged), f"Ошибка парсера: {e}"

    def _fallback_tree(self, tagged):
        children = [Tree(tag, [w]) for w, tag in tagged]
        return Tree("S", children).pformat(margin=80)
