import re
from uuid import UUID
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class LoginUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
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

    username: str = Field(min_length=3, max_length=25)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=25)
    avatar: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str = Field(min_length=3, max_length=25)
    email: EmailStr = Field(max_length=255)
    avatar: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
