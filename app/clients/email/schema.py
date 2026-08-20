from pydantic import BaseModel, EmailStr


class EmailBase(BaseModel):
    email: EmailStr
    name: str

