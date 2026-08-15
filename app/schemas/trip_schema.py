from pydantic import BaseModel


class TripService(BaseModel):
    destination: str
    date: str
    duration: str

class TripResponse(TripService):
    pass

class UpdateTrip(BaseModel):
    pass

class PlanTrip(TripService):
    first_name:str
    last_name:str
    email: str
    phone_number: str
    number_of_golfers: int
    number_of_non_golfers: int
    golf_rounds: int
    hotel_preference: str
    airport_transfers: bool
    arrange_flights: bool
    flexible_date:bool
    experiences:str
    additional_specifications:str
    budget: str


class PlanTripResponse(PlanTrip):
        id: int
        first_name: str
        last_name: str
        email:str
        phone_number: str

        model_config = {
            "from_attributes": True
        }

class PlanTripUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    number_of_golfers: int | None = None
    number_of_non_golfers: int | None = None
    golf_rounds: int | None = None
    hotel_preference: str| None = None
    airport_transfers: bool | None = None
    arrange_flights: bool | None = None
    flexible_date: bool | None = None
    experiences: str | None = None
    additional_specifications: str | None = None
    budget: str | None = None





