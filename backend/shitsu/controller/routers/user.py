from fastapi import APIRouter, Depends, Response

from backend.shitsu.app.schemas.user import LoginUser, RegisterSchema
from backend.shitsu.app.utils.token import (current_access_token,
                                            current_refresh_token)
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


@user.get("/veryfy")
async def verify(token: str):
    return await UserService.verify_user(token)
