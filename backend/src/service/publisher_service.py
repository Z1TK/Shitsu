from fastapi import HTTPException

from backend.src.app.repository.publisher_repo import PublisherRepository
from backend.src.app.schemas.publisher import (PublisherCreateSchema,
                                               PublisherIdschema,
                                               PublisherReadSchema,
                                               PublisherUpdateSchema)


class PublisherService:

    @staticmethod
    async def get_all_publishers(page: int, limit: int):
        publishers = await PublisherRepository.get_all(page=page, limit=limit)
        if not publishers:
            raise HTTPException(status_code=404, detail="Publishers not found")
        return [
            PublisherReadSchema.model_validate(author).model_dump()
            for author in publishers
        ]

    @staticmethod
    async def get_publisher_by_id(publisher_id: str):
        publisher = await PublisherRepository.get_publisher_title(model_id=publisher_id)
        if not publisher:
            raise HTTPException(status_code=404, detail="Publisher not found")
        return PublisherIdschema.model_validate(publisher).model_dump()

    @staticmethod
    async def add_publisher(dto: PublisherCreateSchema):
        value = dto.model_dump()
        publisher = await PublisherRepository.add(**value)
        if not publisher:
            raise HTTPException(status_code=400, detail="Failed to create publisher")
        return PublisherReadSchema.model_validate(publisher).model_dump()

    @staticmethod
    async def update_publisher(publisher_id: str, dto: PublisherUpdateSchema):
        value = dto.model_dump(exclude_unset=True)
        publisher = await PublisherRepository.update_by_id(
            model_id=publisher_id, **value
        )
        if not publisher:
            raise HTTPException(status_code=404, detail="Publisher not found")
        return PublisherReadSchema.model_validate(publisher).model_dump()

    @staticmethod
    async def delete_publishers(publisher_ids: list[str]):
        await PublisherRepository.delete_one_or_many(model_ids=publisher_ids)
