from sqlalchemy import Column, String
from app.db.database import Base

class Contacts(Base):
    __tablename__ = 'contacts'
    name = Column(String)
    email = Column(String)
    message = Column(String)