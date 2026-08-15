from sqlalchemy import Column, String, Integer

from app.db.database import Base

class Email(Base):
    __tablename__ = "email"
    id = Column(Integer, primary_key=True)
    email = Column(String)