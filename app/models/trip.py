from sqlalchemy import JSON, Column, String, Integer, Boolean

from app.db.database import Base


class Trip(Base):
    __tablename__ = 'plan_trip'
    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    golfers = Column(Integer)
    date =Column(String)
    non_golfers = Column(Integer)
    rounds = Column(Integer)
    hotel = Column(String)
    airport_transfers = Column(Boolean)
    flights = Column(Boolean)
    flexible_dates = Column(Boolean)
    experiences = Column(JSON, default=list)
    destination =Column(String)
    other_destination = Column(String)
    additional_specifications = Column(String)
    continent = Column(String)
    budget = Column(String)

