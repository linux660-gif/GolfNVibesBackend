from fastapi import APIRouter
from sqlalchemy import select
import logging


from  app.schemas.tournament_schema import TournamentHost as TournamentHostSchema
from app.db.database import get_db
from app.models.tournament import Tournament as TournamentModel
from app.clients.email.email_service import EmailService

router = APIRouter(prefix = "/tournament/host", tags = ["Tournament"] )
logger = logging.getLogger(__name__)
email_service = EmailService()

@router.post("/")
async def host_tournament(tournament:TournamentHostSchema):
    async with get_db as db:
        result = db.execute(select(TournamentModel.email).where(TournamentModel.email == tournament.email))
        existing_host = result.scalars().all()
        
        if not existing_host:
            try:
                new_host = TournamentModel(tournament)
                db.add(new_host)
                await db.commit()
                logger.info("Host Added")
                try:
                   await email_service.send_host_confirmation(tournament.email, tournament.company, tournament.full_name)
                   logger.info("Confirmation Email Sent")
                except Exception:
                    logger.error("Confirmation Email not Sent")
                db.refresh(new_host)
                return {
                    "message": "Host Added Successfully!"
                }

            except Exception:
                await db.rollback()
                logger.exception("Server Error")
                return {
                    "message": "Server Error"
                }

        return {
            "message" : "Host Already Exists"
        }








