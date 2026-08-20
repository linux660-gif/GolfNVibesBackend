from pydantic import BaseModel, EmailStr

class MemberBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    handicap_index:str
    club:str
    joining_insight:str

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    full_name: str | None
    email: EmailStr | None
    phone_number: str | None
    handicap_index:str | None
    club:str | None

class MemberResponse(MemberBase):
    pass

class MemberDelete(MemberBase):
    pass

