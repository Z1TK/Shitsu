from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from backend.shitsu.app.schemas.title import TitleReadAllSchema


class PublisherCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(max_length=255)
    another_name: str | None = Field(max_length=255, default=None)
    description: str | None = None
    image: str | None = None


class PublisherUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(max_length=255, default=None)
    another_name: str | None = Field(max_length=255, default=None)
    description: str | None = None
    image: str | None = None


class PublisherReadSchema(PublisherCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class PublisherIdschema(PublisherReadSchema):
    model_config = ConfigDict(from_attributes=True)

    titles: list["TitleReadAllSchema"]
