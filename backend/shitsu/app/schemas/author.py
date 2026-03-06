import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from backend.shitsu.app.schemas.title import TitleReadAllSchema


class AuthorCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(max_length=255)
    pseudunym: str | None = Field(max_length=255, default=None)
    description: str | None = None
    image: str | None = None


class AuthorUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(max_length=255, default=None)
    pseudunym: str | None = Field(max_length=255, default=None)
    description: str | None = None
    image: str | None = None


class AuthorReadSchema(AuthorCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[uuid.UUID, Field()]


class AuthorIdSchema(AuthorReadSchema):
    model_config = ConfigDict(from_attributes=True)

    titles: list["TitleReadAllSchema"]
