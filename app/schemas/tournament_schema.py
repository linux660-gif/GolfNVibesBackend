from pydantic import BaseModel

class TournamentBase(BaseModel):
    pass


class TournamentCreate(TournamentBase):
    pass


class TournamentUpdate(TournamentBase):
    pass


class TournamentResponse(TournamentBase):
    pass


class TournamentHost(TournamentBase):
    full_name:str
    email: str
    company:str
    category:str
    expected_guest:str
    vision:str


