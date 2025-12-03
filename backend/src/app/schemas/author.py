from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
import uuid

# from .title import TitleReadAllSchema


class AuthorCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Annotated[str, Field(max_length=255)]
    pseudunym: Annotated[str | None, Field(max_length=255, default=None)]
    description: Annotated[str | None, Field(default=None)]
    image: Annotated[str | None, Field(default=None)]


class AuthorUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Annotated[str | None, Field(max_length=255)] = None
    pseudunym: Annotated[str | None, Field(max_length=255)] = None
    description: Annotated[str | None, Field()] = None
    image: Annotated[str | None, Field()] = None


class AuthorReadSchema(AuthorCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[uuid.UUID, Field()]


class AuthorIdSchema(AuthorReadSchema):
    model_config = ConfigDict(from_attributes=True)

    titles: list["TitleReadAllSchema"]
