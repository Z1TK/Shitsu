from backend.shitsu.core.celery import app
from backend.shitsu.core.config import settings
from backend.shitsu.app.utils.token import create_token
from datetime import timedelta
from fastapi_mail import MessageSchema, FastMail, MessageType
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import asyncio
from backend.shitsu.core.email import conf

template_dir = Path(__file__).resolve().parent

env = Environment(loader=FileSystemLoader(template_dir))

letter_template = env.get_template("letter.html")


@app.task
def send_verification_email(email: str, token: str):
    link = f"http://localhost:8000/account/verify?token={token}"
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

def send_email(email: str, user_id: str):
    expire_time = timedelta(days=settings.VERIFY_TIME)
    token = create_token(data={"sub": str(user_id)}, expires_delta=expire_time})
    send_verification_email.delay(email, token)