from fastapi import APIRouter, Query
from typing import Annotated

from ...app.schemas import GenreReadSchema
from ...app.dao import GenreDAO

genre = APIRouter(prefix="/genres")


@genre.get("")
async def get_all(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, gl=100)] = 10,
):
    genres = await GenreDAO.get_all(page=page, limit=limit)
    res = [GenreReadSchema.model_validate(genre).model_dump() for genre in genres]
    return res
