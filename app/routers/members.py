from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
import logging


from app.db.database import get_db
from app.routers.trip import email_service
from app.schemas.member_schema import ( MemberCreate as MemberCreateSchema, MemberUpdate)
from app.models.member import Members as MembersModel

router = APIRouter(prefix="/members", tags=["Members"])
logger = logging.getLogger(__name__)

@router.post("/")
async def create_member(member: MemberCreateSchema):
    async with get_db() as db:
        result = await db.execute(select(MembersModel).where(MembersModel.phone_number == member.phone_number))
        existing_member = result.scalars().first()
        if existing_member is None:
            try:
                db.add(member)
                await db.commit()
                await db.refresh(member)
                logger.info("Member created")
                await email_service.send_membership_confirmation(member.email, member.club, member.full_name)
                return {
                    "message": "Member successfully created"
                }
            except Exception as e:
                await db.rollback()
                logger.exception("Server Error")
                return {
                    "message": "Member creation failed",
                    "exception": e
                }
        return {
            "message": "Member Already Exists",
        }

@router.get("/")
async def get_members(member_id: int | None = None, limit: int = 100, offset: int = 0, member_email: str | None = None, member_phone_number: str | None = None):
    async with get_db() as db:
        query = select(MembersModel)
        if member_id is not None:
            query = query.where(MembersModel.phone_number == member_id)
        if member_email is not None:
            query = query.where(MembersModel.email == member_email)
        if member_phone_number is not None:
            query = query.where(MembersModel.phone_number == member_phone_number)
        query = query.offset(offset).limit(limit)

        result = await db.execute(query)

        members = result.scalars().all()

        if not members:
            logger.warning("Member Not Found")
            return {
                "message": "Member Not Found",
            }
        logger.info(f"Member found: {members}")
        return members


@router.patch("/")
async def update_members(update: MemberUpdate, member_id: int | None = None, limit: int = 100, offset: int = 0, member_email: str | None = None,
                      member_phone_number: str | None = None, ):
    async with get_db() as db:
        query = select(MembersModel)
        if member_id is not None:
            query = query.where(MembersModel.phone_number == member_id)
        if member_email is not None:
            query = query.where(MembersModel.email == member_email)
        if member_phone_number is not None:
            query = query.where(MembersModel.phone_number == member_phone_number)
        query = query.offset(offset).limit(limit)

        result = await db.execute(query)

        member = result.scalars().first()

        update_member = update.model_dump(exclude_unset=True)

        allowed_fields = ["full_name", "phone_number", "email", "handicap_index", "club"]

        for field, value in update_member.items():
            if field in allowed_fields:
                setattr(member, field, value)
        try:
            await db.commit()
            await db.refresh(member)
            logger.info("Member Updated")
            return {
                "message": "Member Updated Successfully"
            }
        except Exception as e:
            logging.exception("Database Error")
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.delete("/")
async def delete_members(member_id: int | None = None, limit: int = 100, offset: int = 0,
                         member_email: str | None = None,
                         member_phone_number: str | None = None, ):
    async with get_db() as db:
        query = select(MembersModel)
        if member_id is not None:
            query = query.where(MembersModel.phone_number == member_id)
        if member_email is not None:
            query = query.where(MembersModel.email == member_email)
        if member_phone_number is not None:
            query = query.where(MembersModel.phone_number == member_phone_number)
        query = query.offset(offset).limit(limit)

        result = await db.execute(query)

        member = result.scalars().all()

        try:
            await db.delete(member)
            await db.commit()
            await db.refresh(member)
            logger.info("Member Deleted")
            return {
                "message": "Member Deleted Successfully"
            }
        except Exception as e:
            logging.exception("Database Error")
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")




