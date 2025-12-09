from fastapi import HTTPException, status, Depends, Request
from pydantic import EmailStr
import jwt
from datetime import datetime, timezone

from .password import verify_password
from ..dao.dao import UserDAO
from .token import get_token, validate_token
from ...core.config import settings


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.get_by_email(model_email=email)

    if not user or verify_password(password, user.password) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password"
        )
    return user


def current_access_token(req: Request):
    token = get_token(req, 'access_token')
    return validate_token(token)

def current_refresh_token(req: Request):
    token = get_token(req, 'refresh_token')
    return validate_token(token)
