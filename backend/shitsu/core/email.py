from backend.shitsu.core.config import settings
from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)