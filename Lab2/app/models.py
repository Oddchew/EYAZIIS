from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String, nullable=True)
    content = Column(Text)
    file_type = Column(String)
    meta_data = Column(JSON, default=dict) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_processed = Column(Boolean, default=False)
    
    tokens = relationship("Token", back_populates="document", cascade="all, delete-orphan")


class Token(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    
    word_form = Column(String, index=True)
    lemma = Column(String, index=True)
    pos = Column(String, index=True)
    grammemes = Column(JSON, default=list)
    position = Column(Integer)
    sentence_id = Column(Integer, default=0)
    
    document = relationship("Document", back_populates="tokens")


class Concordance(Base):
    __tablename__ = "concordances"
    
    id = Column(Integer, primary_key=True)
    query = Column(String, index=True)
    query_type = Column(String)
    results = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())