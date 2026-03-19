from fastapi import APIRouter, Depends, Response, Query, Body

from backend.shitsu.app.schemas.user import (
    LoginUser,
    RegisterSchema,
    EmailReset,
    PasswordReset,
)
from backend.shitsu.app.utils.token import current_access_token, current_refresh_token
from backend.shitsu.service.user_service import UserService

user = APIRouter(prefix="/account")


@user.post("/sign_up")
async def register(
    res: Response,
    user_data: RegisterSchema,
):
    return await UserService.register_user(res, user_data)


@user.post("/sign_in")
async def login(res: Response, login_data: LoginUser):
    return await UserService.login_user(res, login_data)


@user.post("/refresh_token")
async def update_access_token(
    res: Response, user_id: str = Depends(current_refresh_token)
):
    return await UserService.update_access_token(res, user_id)


@user.get("/profile")
async def get_profile(user_id: str = Depends(current_access_token)):
    return await UserService.get_user(user_id)


@user.post("/logout")
async def logout(res: Response):
    await UserService.logout_user(res)
    return {"message": "logged out"}


@user.get("/verify")
async def verify(token: str):
    return await UserService.verify_user(token)


@user.post("/email_reset_password")
async def send_email_reset(data: EmailReset):
    await UserService.email_reset_password(data.email)


@user.post("/change_password")
async def change_password(res: Response, token: str, data: PasswordReset):
    return await UserService.change_password(res, data.password, token)
