from sqlalchemy import Column, String
from app.db.database import Base

class Tournaments(Base):
    __tablename__ = 'host_tournament'
    full_name:str = Column(String)
    email: str = Column(String)
    company:str = Column(String)
    category:str = Column(String)
    expected_guest:str = Column(String)
    vision:str = Column(String)