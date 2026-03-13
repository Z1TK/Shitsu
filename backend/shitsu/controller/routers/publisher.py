from typing import Annotated

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from backend.shitsu.app.schemas.publisher import (PublisherCreateSchema,
                                                  PublisherUpdateSchema)
from backend.shitsu.service.publisher_service import PublisherService

publisher = APIRouter(prefix="/publishers")


@publisher.get("")
async def get_all_publisher(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, gl=100)] = 10,
):
    return await PublisherService.get_all_publishers(page, limit)


@publisher.get("/{publisher_id}")
async def get_by_id(publisher_id: str):
    return await PublisherService.get_publisher_by_id(publisher_id)


@publisher.post("")
async def add_publisher(
    publisher_data: PublisherCreateSchema,
):
    return await PublisherService.add_publisher(publisher_data)


@publisher.patch("/{publisher_id}")
async def update_publisher(publisher_data: PublisherUpdateSchema, publisher_id: str):
    return await PublisherService.update_publisher(publisher_id, publisher_data)


@publisher.delete("")
async def delete_publishers(publisher_ids: list[str]):
    await PublisherService.delete_publishers(publisher_ids)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "The deletion was successful."},
    )
