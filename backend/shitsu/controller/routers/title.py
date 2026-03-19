from typing import Annotated

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from backend.shitsu.app.schemas.title import TitleCreateSchema, TitleUpdateSchema
from backend.shitsu.service.title_service import TitleService

title = APIRouter(prefix="/titles")


@title.get("/catalog")
async def get_all(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    type: Annotated[list[str] | None, Query()] = None,
    status: Annotated[list[str] | None, Query()] = None,
    release_format: Annotated[list[str] | None, Query()] = None,
    genres: Annotated[list[int] | None, Query()] = None,
    tags: Annotated[list[int] | None, Query()] = None,
    year_min: int | None = None,
    year_max: int | None = None,
    genres_soft_search: bool | None = None,
    tags_soft_search: bool | None = None,
):
    return await TitleService.get_all_titles(
        page,
        limit,
        type,
        status,
        release_format,
        genres,
        tags,
        year_min,
        year_max,
        genres_soft_search,
        tags_soft_search,
    )


@title.get("/{title_id}")
async def get_by_id(title_id: int, section: str = "info"):
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
