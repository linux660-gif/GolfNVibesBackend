import logging
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig, MessageType
from pydantic import SecretStr


from app.core.config import email_setting

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):

        self.conf = ConnectionConfig(
            MAIL_USERNAME = email_setting.mail_username,
            MAIL_PASSWORD=SecretStr(email_setting.mail_password),
            MAIL_FROM=email_setting.mail_from,
            MAIL_PORT= email_setting.mail_port,
            MAIL_SERVER= email_setting.mail_server,
            MAIL_STARTTLS= email_setting.mail_starttls,
            MAIL_SSL_TLS= email_setting.mail_ssl_tls,
            USE_CREDENTIALS=email_setting.use_credentials,
            VALIDATE_CERTS= email_setting.validate_certs,
            TEMPLATE_FOLDER=Path(__file__).parent / "templates",
        )
        self.fm = FastMail(self.conf)

    async def send_email(self, subject:str, recipient, file_name:str, template_data:dict) -> bool:
        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            template_body= template_data,
            subtype=MessageType.html
        )

        try:
            await self.fm.send_message(message, template_name=file_name)
            return True

        except Exception as e:
            return False


    async def send_welcome_email(self,recipient) -> bool:
        template_data = {
            "name": recipient.split("@")[0],

        }

        message = MessageSchema(
            subject="Welcome To GolfNVibes Newsletter, You are on the List",
            recipients=[recipient],
            template_body=template_data,
            subtype=MessageType.html
        )

        try:
            await self.fm.send_message(message, template_name="welcome.html")
            return True
        except Exception as e:
            return False

    async def send_plan_trip_confirmation(self,recipient,destination, first_name, second_name) -> bool:
        template_data = {
            "reference_number": "ref",
            "name": first_name + second_name,
            "destination": destination,
           


        }

        message = MessageSchema(
            subject=f"Your Custom Travel For {destination} has been received",
            recipients=[recipient],
            template_body=template_data,
            subtype=MessageType.html
        )

        try:
            await self.fm.send_message(message, template_name="plan_trip_confirmation.html")
            return True
        except Exception:
            return False



    async def send_membership_confirmation(self,recipient,club, full_name) -> bool:
        template_data = {
            
            "name": full_name,
            "club": club,

        }

        message = MessageSchema(
            subject=f"Welcome your Membership in {club} is Received",
            recipients=[recipient],
            template_body=template_data,
            subtype=MessageType.html
        )

        try:
            logger.info("Sending....")
            await self.fm.send_message(message, template_name="membership_confirmation.html")
            
            return True
        except Exception:
            logger.exception("Email not Sent!")
            return False


    
    async def send_host_confirmation(self,recipient,company, full_name) -> bool:
        template_data = {
            
            "name": full_name,
            "company": company,

        }

        message = MessageSchema(
            subject="Application Received: GolfNVibes Tournament Host Request",
            recipients=[recipient],
            template_body=template_data,
            subtype=MessageType.html
        )

        try:
            await self.fm.send_message(message, template_name="host_confirmation.html")
            return True
        except Exception:
            return False








