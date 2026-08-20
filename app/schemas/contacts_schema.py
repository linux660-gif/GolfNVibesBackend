from pydantic import BaseModel

class ContactBase(BaseModel):
    name:str
    email:str
    message:str

class ContactCreate(ContactBase):
    pass


class ContactResponse(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass


    