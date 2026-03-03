from typing import Annotated

from fastapi import APIRouter, Query

from backend.src.service.tag_genre_service import TagService

tag = APIRouter(prefix="/tags")


@tag.get("")
async def get_all_tags(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, gl=100)] = 10,
):
    return await TagService.get_all_tags(page, limit)
