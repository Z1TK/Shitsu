import re
import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class LoginUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: Annotated[EmailStr, Field()]
    password: Annotated[str, Field(min_length=8, max_length=25)]

    @field_validator("email", mode="after")
    @classmethod
    def val_email(cls, v: str):
        email = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
        if not email.match(v):
            raise ValueError("Login must be a valid email address")
        return v.lower()


class RegisterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: Annotated[str, Field(min_length=3, max_length=25)]
    email: Annotated[EmailStr, Field(max_length=255)]
    password: Annotated[str, Field(min_length=8, max_length=25)]
    avatar: Annotated[str, Field()]


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[uuid.UUID, Field()]
    username: Annotated[str, Field(min_length=3, max_length=25)]
    email: Annotated[EmailStr, Field(max_length=255)]
    avatar: Annotated[str, Field()]


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
