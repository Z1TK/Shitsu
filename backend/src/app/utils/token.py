import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Request, HTTPException, status, Response

from ...core.config import settings


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encode_jwt


def get_token(req: Request, token_name: str):
    token = req.cookies.get(token_name)
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

def set_cookies(res: Response, user_id: str, token_name: str, max_age: int):
    if token_name == 'access_token':
        token_expire = timedelta(minutes=settings.ACCESS_TIME)
    else:
        token_expire = timedelta(days=settings.REFRESH_TIME)

    token = create_token(
        data={'sub': str(user_id)}, expires_delta=token_expire
    )

    res.set_cookie(
        key=token_name, value=token, httponly=True, max_age=max_age
    )

    return token