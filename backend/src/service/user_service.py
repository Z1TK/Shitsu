from fastapi import HTTPException, Response, status

from backend.src.app.repository.user_repo import UserRepository
from backend.src.app.schemas.user import UserRead, LoginUser, RegisterSchema, Token
from backend.src.app.utils.password import hash_password, verify_password
from backend.src.app.utils.token import set_cookies

class UserService:

    @staticmethod
    async def register_user(res: Response, dto: RegisterSchema):
        values = dto.model_dump()
        exist_user = await UserRepository.get_by_email(model_email=values['email'])
        if exist_user:
            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User exist")
        values['password'] = hash_password(dto.password)
        user = await UserRepository.add(**values)
        access_token = set_cookies(res, user.id, 'access_token', 420)
        refresh_token = set_cookies(res, user.id, 'refresh_token', 1296000)
        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )
    
    @staticmethod
    async def login_user(res: Response, login_data: LoginUser):
        user = await UserRepository.get_by_email(model_email=login_data.email)
        if not user or verify_password(login_data.password, user.password) is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password"
            )
        access_token = set_cookies(res, user.id, 'access_token', 420)
        refresh_token = set_cookies(res, user.id, 'refresh_token', 1296000)
        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )
    
    @staticmethod
    async def get_user(user_id: str):
        user = await UserRepository.get_by_id(model_id=user_id)
        return UserRead.model_validate(user)
    
    @staticmethod
    async def update_access_token(res: Response, user_id: str):
        new_token = set_cookies(res, user_id, 'access_token', 420)
        return {'access_token': new_token, 'token_type': 'bearer'}
    
    @staticmethod
    async def logout_user(res: Response):
        res.delete_cookie(key='access_token', httponly=True)
        res.delete_cookie(key='refresh_token', httponly=True)