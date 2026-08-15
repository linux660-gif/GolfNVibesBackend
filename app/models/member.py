from sqlalchemy import Column, String, Integer

from app.db.database import Base

class Members(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    handicap_index = Column(String)
    club = Column(String)

