from fastapi import APIRouter, Query
from typing import Annotated

from ...app.schemas import TagReadSchema
from ...app.dao import TagDAO

tag = APIRouter(prefix="/tags")


@tag.get("")
async def get_all(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, gl=100)] = 10,
):
    tags = await TagDAO.get_all(page=page, limit=limit)
    res = [TagReadSchema.model_validate(tag).model_dump() for tag in tags]
    return res
