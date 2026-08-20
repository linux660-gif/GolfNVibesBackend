from fastapi import APIRouter, status
import logging
from app.clients.email.email_service import EmailService


from app.clients.email.schema import EmailBase as EmailBaseSchema

router = APIRouter(prefix="/email", tags=["Email"])
logger = logging.getLogger(__name__)
email_service = EmailService()







@router.post("/", status_code=status.HTTP_200_OK)
async def send_email(email: EmailBaseSchema):
    try:
        logger.info(f"Sending email")
        await email_service.send_welcome_email(email.email)
        logger.info("Email Sent")
        return {"message": "Email sent successfully"}
    except Exception as e:
        logger.exception("Email Not Sent")
        return {"message": "Email Not Sent"}










