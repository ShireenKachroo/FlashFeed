#SQLAlchemy ORM models (tables)

from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class ArticleModel(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    source_name = Column(String, nullable=False)  
    category = Column(String, nullable=False)   
    summary = Column(Text, nullable=True)        
    published_at = Column(DateTime, default=datetime.utcnow)