from fastapi import APIRouter

from app.schemas.contacts_schema import ContactCreate 



router = APIRouter(prefix ="/contact", tags = ['Contact'])

@router.post('/')
async def add_contact(messageschema:ContactCreate ):
    pass