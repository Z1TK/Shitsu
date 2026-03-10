from backend.shitsu.core.celery import celery_app
from backend.shitsu.core.config import settings
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail, MessageType
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import asyncio

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

template_dir = Path(__file__).resolve().parent

env = Environment(loader=FileSystemLoader(template_dir))

letter_template = env.get_template("letter.html")


@celery_app.task
def send_verification_email(email: str, token: str):
    link = f"http://localhost:8000/verify?token={token}"
    message = letter_template.render(verification_link=link)
    message = MessageSchema(
        subject="Verification user",
        recipients=[email],
        from_email=settings.MAIL,
        body=message,
        subtype=MessageType.html,
    )

    async def _send():
        fm = FastMail(conf)
        await fm.send_message(message)

    asyncio.run(_send())
