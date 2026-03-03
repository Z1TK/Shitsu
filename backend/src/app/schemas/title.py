import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from backend.src.app.enum.title_enum import *

# from .author import AuthorTitleSchema
# from .publisher import PublisherTitleSchema
# from .genre import GenreReadSchema
# from .tag import TagReadSchema


class TitleReadAllSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field()]
    title: Annotated[str, Field(max_length=255)]
    cover: Annotated[str, Field()]


class TitleCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    title: Annotated[str, Field(max_length=255)]
    description: Annotated[str, Field()]
    alternative_title: Annotated[str | None, Field(max_length=255, default=None)]
    cover: Annotated[str, Field()]
    release_year: Annotated[int, Field()]
    type: Annotated[TypeEnum, Field()]
    status: Annotated[StatusEnum, Field()]
    release_format: Annotated[ReleaseEnum, Field()]
    author_id: Annotated[uuid.UUID, Field()]
    publisher_id: Annotated[uuid.UUID, Field()]
    genres: Annotated[list[int], Field()]
    tags: Annotated[list[int], Field()]


class PublisherTitleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[uuid.UUID, Field()]
    name: Annotated[str, Field(max_length=255)]


class AuthorTitleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[uuid.UUID, Field()]
    name: Annotated[str, Field(max_length=255)]


class TitleReadIDSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: Annotated[int, Field()]
    title: Annotated[str, Field(max_length=255)]
    description: Annotated[str, Field()]
    alternative_title: Annotated[str | None, Field(max_length=255)]
    cover: Annotated[str, Field()]
    release_year: Annotated[int, Field()]
    type: Annotated[TypeEnum, Field()]
    status: Annotated[StatusEnum, Field()]
    release_format: Annotated[ReleaseEnum, Field()]
    author: AuthorTitleSchema
    publisher: PublisherTitleSchema
    genres: list["GenreReadSchema"]
    tags: list["TagReadSchema"]


class TitleUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    title: Annotated[str | None, Field(max_length=255)] = None
    description: Annotated[str | None, Field()] = None
    alternative_title: Annotated[str | None, Field(max_length=255)] = None
    cover: Annotated[str | None, Field(max_length=255)] = None
    release_year: Annotated[int | None, Field()] = None
    type: Annotated[TypeEnum | None, Field()] = None
    status: Annotated[StatusEnum | None, Field()] = None
    release_format: Annotated[ReleaseEnum | None, Field()] = None
    author_id: Annotated[uuid.UUID | None, Field()] = None
    publisher_id: Annotated[uuid.UUID | None, Field()] = None
    # genres: Annotated[list[int] | None, Field()] = None
    # tags: Annotated[list[int] | None, Field()] = None
