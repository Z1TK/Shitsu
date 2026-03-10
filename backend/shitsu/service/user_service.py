from fastapi import HTTPException, Response, status

from backend.shitsu.app.repository.user_repo import UserRepository
from backend.shitsu.app.schemas.user import UserRead, LoginUser, RegisterSchema, Token
from backend.shitsu.app.utils.password import hash_password, verify_password
from backend.shitsu.app.utils.token import set_cookies
from backend.shitsu.app.logger import log
from backend.shitsu.app.utils.decorators import cached


class UserService:

    @staticmethod
    async def register_user(res: Response, dto: RegisterSchema):
        log.info(f"Registering user: email={dto.email}")
        values = dto.model_dump()
        exist_user = await UserRepository.get_by_email(values["email"])
        if exist_user:
            log.warning(f"User already exists: email={dto.email}")
            return HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User exist"
            )
        values["password"] = hash_password(dto.password)
        user = await UserRepository.add(**values)
        access_token = set_cookies(res, user.id, "access_token", 420)
        refresh_token = set_cookies(res, user.id, "refresh_token", 1296000)
        log.info(f"User registered successfully: id={user.id}, email={dto.email}")
        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    @staticmethod
    async def login_user(res: Response, login_data: LoginUser):
        log.info(f"Login attempt: email={login_data.email}")
        user = await UserRepository.get_by_email(login_data.email)
        if not user or verify_password(login_data.password, user.password) is False:
            log.warning(f"Failed login attempt: email={login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email or password",
            )
        access_token = set_cookies(res, user.id, "access_token", 420)
        refresh_token = set_cookies(res, user.id, "refresh_token", 1296000)
        log.info(f"User logged in successfully: id={user.id}, email={login_data.email}")
        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    @staticmethod
    @cached("cache:user")
    async def get_user(user_id: str):
        log.info(f"Fetching user: id={user_id}")
        user = await UserRepository.get_by_id(user_id)
        log.info(f"Found user: id={user_id}")
        return UserRead.model_validate(user)

    @staticmethod
    async def update_access_token(res: Response, user_id: str):
        log.info(f"Refreshing access token: user_id={user_id}")
        new_token = set_cookies(res, user_id, "access_token", 420)
        log.info(f"Access token refreshed: user_id={user_id}")
        return {"access_token": new_token, "token_type": "bearer"}

    @staticmethod
    async def logout_user(res: Response):
        log.info("User logged out")
        res.delete_cookie(key="access_token", httponly=True)
        res.delete_cookie(key="refresh_token", httponly=True)
