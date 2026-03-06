from typing import Annotated

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from backend.shitsu.app.schemas.author import AuthorCreateSchema, AuthorUpdateSchema
from backend.shitsu.service.author_service import AuthorService

author = APIRouter(prefix="/authors")


@author.get("")
async def get_all_author(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, gl=100)] = 10,
):
    return await AuthorService.get_all_authors(page, limit)


@author.get("/{author_id}")
async def get_by_id(author_id: str):
    return await AuthorService.get_author_by_id(author_id)


@author.post("")
async def add_author(
    author_data: AuthorCreateSchema,
):
    return await AuthorService.add_author(author_data)


@author.patch("/{author_id}")
async def update_author(author_data: AuthorUpdateSchema, author_id: str):
    return await AuthorService.update_author(author_id, author_data)


@author.delete("")
async def delete_authors(author_ids: list[str]):
    await AuthorService.delete_authors(model_ids=author_ids)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "The deletion was successful."},
    )
