from fastapi import APIRouter, HTTPException, status, Response, Depends
from pydantic import EmailStr
from datetime import timedelta

from ...app.schemas import RegisterSchema, Token, LoginUser, UserRead
from ...app.dao import UserDAO
from ...app.utils import (
    hash_password,
    set_tokens_and_cookies,
    create_access_token,
    update_access_token,
    current_user,
    authenticate_user,
)
from ...core import settings

user = APIRouter(prefix="/accounts")


@user.post("/sign_up")
async def register(user_data: RegisterSchema, res: Response):
    exist_user = await UserDAO.get_by_email(model_email=user_data.email)
    if exist_user:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User exist")

    user_data.password = hash_password(user_data.password)
    user = await UserDAO.add(values=user_data)
    access_token, refresh_token = set_tokens_and_cookies(res, user.id)
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@user.post("/sign_in")
async def login(res: Response, login_data: LoginUser):
    user = await authenticate_user(email=login_data.email, password=login_data.password)
    access_token, refresh_token = set_tokens_and_cookies(res, user.id)
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )

@user.post('/refresh_token')
async def update_access_token(res: Response, user_id: str = Depends(update_access_token)):
    access_token_expire = timedelta(minutes=settings.ACCESS_TIME)
    new_access_token = create_access_token(
        data={'sub': user_id}, expires_delta=access_token_expire
    ) 
    res.set_cookie(key='access_token', value=new_access_token, httponly=True, max_age=420)
    return {'access_token': new_access_token, 'token_type': 'bearer'}

@user.get("/profile")
async def get_user(user_id: str = Depends(current_user)):
    user = await UserDAO.get_by_id(model_id=user_id)
    res = UserRead.model_validate(user)
    return res


@user.post('/logout')
async def logout(res: Response):
    res.delete_cookie(key='access_token', httponly=True)
    res.delete_cookie(key='refresh_token', httponly=True)
    return {'message': 'logged out'}
