from sqlalchemy import Column, String, Integer, Boolean

from app.db.database import Base


class Trip(Base):
    __tablename__ = 'plan_trip'
    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    number_of_golfers = Column(Integer)
    number_of_non_golfers = Column(Integer)
    golf_rounds = Column(Integer)
    hotel_preference = Column(String)
    airport_transfers = Column(Boolean)
    arrange_flights = Column(Boolean)
    flexible_date = Column(Boolean)
    experiences = Column(String)
    additional_specifications = Column(String)
    budget = Column(String)

