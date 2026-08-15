from sqlalchemy import Column, Integer, String

from app.db.database import Base

class NewsLetter(Base):
    __tablename__ = 'news_letter'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)


