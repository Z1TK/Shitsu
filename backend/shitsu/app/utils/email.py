from datetime import timedelta
from pathlib import Path

import resend
from jinja2 import Environment, FileSystemLoader

from backend.shitsu.app.utils.token import create_token
from backend.shitsu.core.celery import app
from backend.shitsu.core.config import settings

template_dir = Path(__file__).resolve().parent.parent

env = Environment(loader=FileSystemLoader(template_dir))

verify_email = env.get_template("templates/verify.html")
reset_password = env.get_template("templates/reset_password.html")

resend.api_key = settings.RESEND_KEY


def send_verification_email(email: str, token: str):
    link = f"http://localhost:8000/api/account/verify?token={token}"
    message = verify_email.render(verification_link=link)
    resend.Emails.send(
        {
            "from": settings.MAIL,
            "to": email,
            "subject": "Verification user",
            "html": message,
        }
    )

def new_user_password(email: str, token: str):
    link = f"http://localhost:8000/api/account/change_password?token={token}"
    message = reset_password.render(reset_link=link)
    resend.Emails.send(
        {
            "from": settings.MAIL,
            "to": email,
            "subject": "Password Reset",
            "html": message,
        }
    )

@app.task
def send_email_verify(email: str):
    expire_time = timedelta(days=settings.VERIFY_TIME)
    token = create_token(data={"sub": str(email)}, expires_delta=expire_time)
    send_verification_email(email, token)

@app.task
def send_email_reset(email: str):
    expire_time = timedelta(minutes=settings.RESET_TIME)
    token = create_token(data={"sub": str(email)}, expires_delta=expire_time)
    new_user_password(email, token)
