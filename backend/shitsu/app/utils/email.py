from datetime import timedelta
from pathlib import Path

import resend
from jinja2 import Environment, FileSystemLoader

from backend.shitsu.app.utils.token import create_token
from backend.shitsu.core.celery import app
from backend.shitsu.core.config import settings

template_dir = Path(__file__).resolve().parent

env = Environment(loader=FileSystemLoader(template_dir))

letter_template = env.get_template("letter.html")

resend.api_key = settings.RESEND_KEY


def send_verification_email(email: str, token: str):
    link = f"http://localhost:8000/api/account/verify?token={token}"
    message = letter_template.render(verification_link=link)
    resend.Emails.send(
        {
            "from": settings.MAIL,
            "to": email,
            "subject": "Verification user",
            "html": message,
        }
    )


@app.task
def send_email(email: str, user_id: str):
    expire_time = timedelta(days=settings.VERIFY_TIME)
    token = create_token(data={"sub": str(user_id)}, expires_delta=expire_time)
    send_verification_email(email, token)
