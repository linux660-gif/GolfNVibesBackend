from pydantic import BaseModel


class NewsLetter(BaseModel):
    email: str

class NewsLetterCreate(NewsLetter):
    pass

class NewsLetterUpdate(NewsLetter):
    email: str

class NewsLetterResponse(NewsLetterCreate):
    pass
