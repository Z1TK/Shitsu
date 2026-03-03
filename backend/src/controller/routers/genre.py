from typing import Annotated

from fastapi import APIRouter, Query

from backend.src.service.tag_genre_service import GenreService

genre = APIRouter(prefix="/genres")


@genre.get("")
async def get_all_genres(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, gl=100)] = 10,
):
    return await GenreService.get_all_genres(page, limit)
