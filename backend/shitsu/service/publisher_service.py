from fastapi import HTTPException

from backend.shitsu.app.logger import log
from backend.shitsu.app.repository.publisher_repo import PublisherRepository
from backend.shitsu.app.schemas.publisher import (
    PublisherCreateSchema,
    PublisherIdschema,
    PublisherReadSchema,
    PublisherUpdateSchema,
)
from backend.shitsu.app.utils.cache import delete_cache, delete_pattern_cache
from backend.shitsu.app.utils.decorators import cached


class PublisherService:

    @staticmethod
    @cached("cache:publishers")
    async def get_all_publishers(page: int, limit: int):
        log.info(f"Fetching all publishers: page={page}, limit={limit}")
        publishers = await PublisherRepository.get_all(page, limit)
        if not publishers:
            log.warning("No publishers found")
            raise HTTPException(status_code=404, detail="Publishers not found")
        log.info(f"Found {len(publishers)} publishers")
        return [
            PublisherReadSchema.model_validate(author).model_dump()
            for author in publishers
        ]

    @staticmethod
    @cached("cache:publisher")
    async def get_publisher_by_id(publisher_id: str):
        log.info(f"Fetching publisher by id={publisher_id}")
        publisher = await PublisherRepository.get_publisher_title(publisher_id)
        if not publisher:
            log.warning(f"Publisher id={publisher_id} not found")
            raise HTTPException(status_code=404, detail="Publisher not found")
        log.info(f"Found publisher id={publisher_id}")
        return PublisherIdschema.model_validate(publisher).model_dump()

    @staticmethod
    async def add_publisher(dto: PublisherCreateSchema):
        log.info(f"Creating publisher: {dto.model_dump()}")
        value = dto.model_dump()
        publisher = await PublisherRepository.add(**value)
        if not publisher:
            log.error("Failed to create publisher")
            raise HTTPException(status_code=400, detail="Failed to create publisher")
        await delete_pattern_cache("cache:publishers:*")
        log.info("Publisher created successfully")
        return PublisherReadSchema.model_validate(publisher).model_dump()

    @staticmethod
    async def update_publisher(publisher_id: str, dto: PublisherUpdateSchema):
        log.info(
            f"Updating publisher id={publisher_id}: {dto.model_dump(exclude_unset=True)}"
        )
        value = dto.model_dump(exclude_unset=True)
        publisher = await PublisherRepository.update_by_id(
            model_id=publisher_id, **value
        )
        if not publisher:
            log.warning(f"Publisher id={publisher_id} not found for update")
            raise HTTPException(status_code=404, detail="Publisher not found")
        await delete_cache(f"cache:publisher:{publisher_id}")
        await delete_pattern_cache("cache:publishers:*")
        log.info(f"Publisher id={publisher_id} updated successfully")
        return PublisherReadSchema.model_validate(publisher).model_dump()

    @staticmethod
    async def delete_publishers(publisher_ids: list[str]):
        log.info(f"Deleting publishers: {publisher_ids}")
        await PublisherRepository.delete_one_or_many(model_ids=publisher_ids)
        await delete_pattern_cache("cache:publishers:*")
        log.info(f"Publishers deleted successfully: {publisher_ids}")
