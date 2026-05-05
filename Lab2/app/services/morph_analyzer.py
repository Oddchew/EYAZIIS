# app/services/morph_analyzer.py
import pymorphy3
from typing import List, Optional
from app.models import Token
import re
from nltk.tokenize import sent_tokenize

class MorphAnalyzer:
    def __init__(self):
        self.morph = pymorphy3.MorphAnalyzer(lang='ru')
    
    def analyze_word(self, word: str) -> Optional[dict]:
        """Анализ отдельного слова через pymorphy3"""
        parsed = self.morph.parse(word)[0]
        return {
            'word_form': word,
            'lemma': parsed.normal_form,
            'pos': parsed.tag.POS,
            'grammemes': list(parsed.tag.grammemes),
            'score': parsed.score
        }
    
    def analyze_text(self, text: str, doc_id: int, sentence_splitter=None) -> List[Token]:
        """Токенизация и морфологический анализ текста"""
        tokens = []
        position = 0
        
        sentences = sent_tokenize(text, language='russian') if sentence_splitter is None else sentence_splitter(text)
        
        for sent_id, sentence in enumerate(sentences):
            # Токенизация с сохранением пунктуации
            words = re.findall(r'\b\w+\b|[^\w\s]', sentence, re.UNICODE)
            
            for word in words:
                if not word.strip():
                    continue
                    
                analysis = self.analyze_word(word)
                if analysis:
                    token = Token(
                        document_id=doc_id,
                        word_form=word,
                        lemma=analysis['lemma'],
                        pos=analysis['pos'] or 'X',
                        grammemes=analysis['grammemes'],
                        position=position,
                        sentence_id=sent_id
                    )
                    tokens.append(token)
                    position += 1
        
        return tokens