from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from ..database import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    extracted_text = Column(Text, nullable=False)  # Full resume text
    skills = Column(JSON, nullable=True)  # Extracted skills as JSON
    embedding_id = Column(String(100), nullable=True)  # FAISS index reference
    created_at = Column(DateTime, default=datetime.utcnow)