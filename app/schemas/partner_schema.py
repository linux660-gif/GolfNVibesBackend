from pydantic import BaseModel

class PartnerBase(BaseModel):
    organization: str
    partnership_type: str
    email:str
    details:str

class PartnerCreate(PartnerBase):
    pass


class PartnerResponse(PartnerBase):
    pass


class PartnerUpdate(PartnerBase):
    pass


