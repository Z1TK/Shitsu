from fastapi import HTTPException, status, Depends, Request
from pydantic import EmailStr
import jwt
from datetime import datetime, timezone

from .password import verify_password
from backend.src.app.repository.user_repo import UserRepository
from backend.src.app.utils.token import get_token, validate_token
from ...core.config import settings


def current_access_token(req: Request):
    token = get_token(req, 'access_token')
    return validate_token(token)

def current_refresh_token(req: Request):
    token = get_token(req, 'refresh_token')
    return validate_token(token)
