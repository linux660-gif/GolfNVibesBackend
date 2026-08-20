from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
import logging

from app.db.database import  get_db
from app.models.newsletter import NewsLetter as NewsLetterModel
from app.schemas.newletter_schema import NewsLetterCreate, NewsLetterUpdate
from app.clients.email.email_service import EmailService



router = APIRouter(prefix="/newsletter" ,tags=['Newsletter'])
logger = logging.getLogger(__name__)
email_service = EmailService()



@router.post("/", tags=['Newsletter'], response_model=None)
async def add_subscriber(user:NewsLetterCreate):
    async with get_db() as db:
       result = await db.execute(
        select(NewsLetterModel).where(NewsLetterModel.email == user.email)
    )
       existing_subscriber = result.scalars().first()
       if not existing_subscriber:
           try:
                new_subscriber =NewsLetterModel(email=user.email)
                db.add(new_subscriber)
                await db.commit()
                db.refresh(new_subscriber)
                await email_service.send_welcome_email(user.email)
                return {"message":"Email Added Successfully"}
           except Exception as e:
               logger.exception("Server Error")
               await db.rollback()
               return {"message":"Server Error"}

       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

@router.delete("/{email_id}", tags=['Newsletter'], response_model=None)
async def delete_subscriber(email_id:int):
    async with get_db() as db:
        result = await db.execute(select(NewsLetterModel).where(NewsLetterModel.id == email_id))
        existing_subscriber = result.scalars().first()
        if not existing_subscriber:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
        await db.delete(existing_subscriber)
        await db.commit()
        return "Email Deleted Successfully"


@router.put('/{email_id}', tags=['Newsletter'], response_model=None)
async def update_subscriber(email_id: int, subscriber:NewsLetterUpdate):
    async with get_db() as db:
        result = await db.execute(select(NewsLetterModel).where(NewsLetterModel.id == email_id))
        existing_subscriber = result.scalars().first()
        if not existing_subscriber:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
        existing_subscriber.email = subscriber.email

        await db.commit()
        await db.refresh(existing_subscriber)
        return "Email Updated Successfully"

@router.get('/', tags=['Newsletter'], response_model=None)
async def get_subscribers():
    async with get_db() as db:
        result = await db.execute(select(NewsLetterModel))
        existing_subscribers = result.scalars().all()
        if not existing_subscribers:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The NewsLetter Is Empty")
        return existing_subscribers


