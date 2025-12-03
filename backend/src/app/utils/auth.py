from fastapi import HTTPException, status, Depends
from pydantic import EmailStr
import jwt
from datetime import datetime, timezone

from .password import verify_password
from ..dao.dao import UserDAO
from .token import get_access_token, get_refresh_token, validate_token
from ...core.config import settings


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.get_by_email(model_email=email)

    if not user or verify_password(password, user.password) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password"
        )
    return user


def current_user(token: str = Depends(get_access_token)):
    return validate_token(token)

def update_access_token(token: str = Depends(get_refresh_token)):
    return validate_token(token)
