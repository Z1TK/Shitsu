from typing import Annotated

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from backend.shitsu.app.schemas.title import TitleCreateSchema, TitleUpdateSchema
from backend.shitsu.service.title_service import TitleService

title = APIRouter(prefix="/titles")


@title.get("")
async def get_all(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    type: Annotated[str | None, Query()] = None,
    status: Annotated[str | None, Query()] = None,
    release_format: Annotated[str | None, Query()] = None,
    genres: Annotated[list[int] | None, Query()] = None,
    tags: Annotated[list[int] | None, Query()] = None,
):
    return await TitleService.get_all_titles(
        page, limit, type, status, release_format, genres, tags
    )


@title.get("/{title_id}")
async def get_by_id(title_id: int):
    return await TitleService.get_title_by_id(title_id)


@title.post("")
async def add(title_data: TitleCreateSchema):
    return await TitleService.add_title(title_data)


@title.patch("/{title_id}")
async def update_title(title_data: TitleUpdateSchema, title_id: int):
    return await TitleService.update_title(title_id, title_data)


@title.delete("")
async def delete_title(title_ids: list[int]):
    await TitleService.delete_titles(title_ids)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "The deletion was successful."},
    )
