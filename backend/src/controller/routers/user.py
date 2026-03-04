from fastapi import APIRouter, Response, Depends

from backend.src.app.schemas.user import RegisterSchema, LoginUser
from backend.src.service.user_service import UserService
from backend.src.app.utils.auth import current_access_token,current_refresh_token

user = APIRouter(prefix="/accounts")


@user.post("/sign_up")
async def register(res: Response, user_data: RegisterSchema, ):
    return await UserService.register_user(res, user_data)


@user.post("/sign_in")
async def login(res: Response, login_data: LoginUser):
    return await UserService.login_user(res, login_data)

@user.post('/refresh_token')
async def update_access_token(res: Response, user_id: str = Depends(current_refresh_token)):
    return await UserService.update_access_token(res, user_id)

@user.get("/profile")
async def get_profile(user_id: str = Depends(current_access_token)):
    return await UserService.get_user(user_id)


@user.post('/logout')
async def logout(res: Response):
    await UserService.logout_user(res)
    return {'message': 'logged out'}
