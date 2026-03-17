from fastapi import HTTPException, Response, status

from backend.shitsu.app.logger import log
from backend.shitsu.app.repository.user_repo import UserRepository
from backend.shitsu.app.schemas.user import (LoginUser, RegisterSchema, Token,
                                             UserRead)
from backend.shitsu.app.utils.decorators import cached
from backend.shitsu.app.utils.email import send_email_reset, send_email_verify
from backend.shitsu.app.utils.password import hash_password, verify_password
from backend.shitsu.app.utils.token import set_cookies, validate_token


class UserService:

    @staticmethod
    async def register_user(res: Response, dto: RegisterSchema):
        log.info(f"Registering user: email={dto.email}")
        values = dto.model_dump()
        exist_user = await UserRepository.get_by_email(values["email"])
        if exist_user:
            log.warning(f"User already exists: email={dto.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User exist"
            )
        values["password"] = hash_password(dto.password)
        user = await UserRepository.add(**values)
        access_token = set_cookies(res, user.id, "access_token", 420)
        refresh_token = set_cookies(res, user.id, "refresh_token", 1296000)
        send_email_verify.delay(user.email, str(user.id))
        log.info(f"User registered successfully: id={user.id}, email={user.email}")
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

    @staticmethod
    async def verify_user(token: str):
        email = validate_token(token)
        user = await UserRepository.update_by_email(model_email=email, is_verified=True)
        if not user:
            log.warning(f"User not found: email={email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return {"message": "Your email has been successfully verified."}
    
    @staticmethod
    async def email_reset_password(email: str):
        send_email_reset.delay(email)

    @staticmethod
    async def change_password(res: Response, password: str, token: str):
        user_email = validate_token(token)
        password = hash_password(password)
        user = await UserRepository.update_by_email(model_email=user_email, password=password)
        if not user:
            log.warning(f"User not found: email={user_email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        log.info("User cookies deleted after password change")
        res.delete_cookie(key="access_token", httponly=True)
        res.delete_cookie(key="refresh_token", httponly=True)
        return {"message": "Password successfully changed"}
        
