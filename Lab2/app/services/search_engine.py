from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from app.models import Token, Document, Concordance
from app.schemas import SearchQuery, ConcordanceItem
import time
import re

class SearchEngine:
    
    @staticmethod
    def search_concordances(db: Session, query: SearchQuery) -> dict:
        """
        Поиск вхождений с контекстом (конкордансы).
        Возвращает результаты + метрики выполнения.
        """
        start_time = time.time()
        
        token_query = db.query(Token).join(Document)

        if query.query_type == "lemma":
            token_query = token_query.filter(Token.lemma.ilike(f"%{query.query}%"))
        elif query.query_type == "word_form":
            token_query = token_query.filter(Token.word_form.ilike(f"%{query.query}%"))
        elif query.query_type == "pos":
            token_query = token_query.filter(Token.pos == query.query.upper())
        elif query.query_type == "regex":
            token_query = token_query.filter(Token.word_form.op("REGEXP")(query.query))
        
        if query.document_id:
            token_query = token_query.filter(Token.document_id == query.document_id)
        
        if query.pos_filter:
            token_query = token_query.filter(Token.pos == query.pos_filter.upper())
        
        tokens = token_query.limit(query.limit).all()
        total_found = token_query.count()  # Общее количество без лимита
        
        results = []
        for token in tokens:
            context = SearchEngine._get_context(db, token, query.context_window)
            
            # Получаем имя файла
            doc = db.query(Document).filter(Document.id == token.document_id).first()
            
            results.append(ConcordanceItem(
                document_id=token.document_id,
                filename=doc.filename if doc else "Unknown",
                position=token.position,
                left_context=context['left'],
                target=token.word_form,
                right_context=context['right'],
                grammemes=token.grammemes
            ))
        
        execution_time = (time.time() - start_time) * 1000  # в миллисекундах
        
        return {
            "query": query.query,
            "total_found": total_found,
            "results": results,
            "execution_time_ms": round(execution_time, 2)
        }
    
    @staticmethod
    def _get_context(db: Session, token: Token, window: int) -> dict:
        """Получение левого и правого контекста для токена"""
        left_tokens = db.query(Token.word_form).filter(
            and_(
                Token.document_id == token.document_id,
                Token.position < token.position,
                Token.position >= token.position - window
            )
        ).order_by(Token.position.desc()).all()
        
        right_tokens = db.query(Token.word_form).filter(
            and_(
                Token.document_id == token.document_id,
                Token.position > token.position,
                Token.position <= token.position + window
            )
        ).order_by(Token.position.asc()).all()
        
        return {
            'left': ' '.join([t[0] for t in reversed(left_tokens)]),
            'right': ' '.join([t[0] for t in right_tokens])
        }
    
    @staticmethod
    def get_document_stats(db: Session, document_id: int) -> dict:
        """Статистика по документу: частоты, POS-распределение и т.д."""
        total_tokens = db.query(func.count(Token.id)).filter(
            Token.document_id == document_id
        ).scalar()
        
        # Уникальные леммы
        unique_lemmas = db.query(func.count(Token.lemma.distinct())).filter(
            Token.document_id == document_id
        ).scalar()
        
        pos_dist_raw = db.query(Token.pos, func.count(Token.id)).filter(
            Token.document_id == document_id
        ).group_by(Token.pos).all()
        pos_distribution = {pos: count for pos, count in pos_dist_raw}
        
        top_lemmas_raw = db.query(Token.lemma, func.count(Token.id)).filter(
            Token.document_id == document_id
        ).group_by(Token.lemma).order_by(
            func.count(Token.id).desc()
        ).limit(10).all()
        top_lemmas = [{"lemma": lemma, "count": count} for lemma, count in top_lemmas_raw]
        
        return {
            "document_id": document_id,
            "total_tokens": total_tokens,
            "unique_lemmas": unique_lemmas,
            "pos_distribution": pos_distribution,
            "top_lemmas": top_lemmas
        }