import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Request, HTTPException, status, Response

from ...core.config import settings


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encode_jwt


def get_access_token(req: Request):
    token = req.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token not found"
        )
    return token

def get_refresh_token(req: Request):
    token = req.cookies.get("refresh_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token not found"
        )
    return token

def validate_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.ALGORITHM,
            options={"verify_exp": True},
        )
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid"
        )
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="ID not found"
        )

    return user_id

def set_tokens_and_cookies(res: Response, id: str):
    access_token_expire = timedelta(minutes=settings.ACCESS_TIME)
    refresh_token_expire = timedelta(days=settings.REFRESH_TIME)

    access_token = create_access_token(
        data={"sub": str(id)}, expires_delta=access_token_expire
    )
    refresh_token = create_access_token(
        data={"sub": str(id)}, expires_delta=refresh_token_expire
    )

    res.set_cookie(
        key="access_token", value=access_token, httponly=True, max_age=420
    )
    res.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, max_age=1296000
    )

    return access_token, refresh_token