from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from backend.shitsu.app.enum.title_enum import *


class TitleReadAllSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str = Field(max_length=255)
    cover: str


class TitleCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    title: str = Field(max_length=255)
    description: str
    alternative_title: str | None = Field(max_length=255, default=None)
    cover: str
    release_year: int
    type: TypeEnum
    status: StatusEnum
    release_format: ReleaseEnum
    author_id: UUID
    publisher_id: UUID
    genres: list[int]
    tags: list[int]


class PublisherTitleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str = Field(max_length=255)


class AuthorTitleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str = Field(max_length=255)


class GenreTitleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: Annotated[str, Field(max_length=255)]


class TagTitleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: Annotated[str, Field(max_length=255)]


class CommentTitleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    content: str
    user_id: UUID
    likes_count: int


class ChapterTitleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    volume: str
    number: float


class TitleReadIDSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    title: Annotated[str, Field(max_length=255)]
    description: str
    alternative_title: str | None = Field(max_length=255)
    cover: str
    release_year: int
    type: TypeEnum
    status: StatusEnum
    release_format: ReleaseEnum
    author: AuthorTitleSchema
    publisher: PublisherTitleSchema
    genres: list[GenreTitleSchema]
    tags: list[TagTitleSchema]
    comments: list[CommentTitleSchema]
    chapters: list[ChapterTitleSchema]


class TitleUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    title: Annotated[str | None, Field(max_length=255)] = None
    description: str | None = None
    alternative_title: Annotated[str | None, Field(max_length=255)] = None
    cover: str | None = None
    release_year: int | None = None
    type: TypeEnum | None = None
    status: StatusEnum | None = None
    release_format: ReleaseEnum | None = None
    author_id: UUID | None = None
    publisher_id: UUID | None = None
    genres: list[int] | None = None
    tags: list[int] | None = None
