from fastapi import HTTPException

from backend.shitsu.app.logger import log
from backend.shitsu.app.repository.tag_genre_repo import (GenreRepository,
                                                          TagRepository)
from backend.shitsu.app.repository.title_repo import TitleRepository
from backend.shitsu.app.schemas.title import (TitleCreateSchema,
                                              TitleReadAllSchema,
                                              TitleReadIDSchema,
                                              TitleUpdateSchema)
from backend.shitsu.app.utils.cache import delete_cache, delete_pattern_cache
from backend.shitsu.app.utils.decorators import cached


class TitleService:

    @staticmethod
    @cached("cache:titles")
    async def get_all_titles(
        page: int,
        limit: int,
        type: str,
        status: str,
        release_format: str,
        genres: list[int],
        tags: list[int],
    ):
        log.info(
            f"Fetching all titles: page={page}, limit={limit}, type={type}, status={status}, release_format={release_format}, genres={genres}, tags={tags}"
        )
        titles = await TitleRepository.get_all(
            page,
            limit,
            type,
            status,
            release_format,
            genres,
            tags,
        )
        if not titles:
            log.warning("No titles found")
            raise HTTPException(status_code=404, detail="Titles not found")
        log.info(f"Found {len(titles)} titles")
        return [
            TitleReadAllSchema.model_validate(title).model_dump() for title in titles
        ]

    @staticmethod
    @cached("cache:title")
    async def get_title_by_id(title_id: str):
        log.info(f"Fetching title by id={title_id}")
        title = await TitleRepository.get_by_id(model_id=title_id)
        if not title:
            log.warning(f"Title id={title_id} not found")
            raise HTTPException(status_code=404, detail="Title not found")
        log.info(f"Found title id={title_id}")
        return TitleReadIDSchema.model_validate(title).model_dump()

    @staticmethod
    async def add_title(dto: TitleCreateSchema):
        log.info(f"Creating title: {dto.model_dump()}")
        value = dto.model_dump()
        genre_ids = value.pop("genres")
        tag_ids = value.pop("tags")
        genres = await GenreRepository.get_by_ids(ids=genre_ids)
        tags = await TagRepository.get_by_ids(ids=tag_ids)
        title_id = await TitleRepository.create(**value, genres=genres, tags=tags)
        if not title_id:
            log.error("Failed to create title")
            raise HTTPException(status_code=400, detail="Failed to create title")
        await delete_pattern_cache("cache:titles:*")
        log.info(f"Title created successfully: id={title_id}")
        return {"id": title_id}

    @staticmethod
    async def update_title(id: str, dto: TitleUpdateSchema):
        log.info(f"Updating title id={id}: {dto.model_dump(exclude_unset=True)}")
        value = dto.model_dump(exclude_unset=True)
        title_id = await TitleRepository.update_by_id(model_id=id, **value)
        if not title_id:
            log.warning(f"Title id={id} not found for update")
            raise HTTPException(status_code=404, detail="Title not found")
        await delete_cache(f"cache:title:{title_id}")
        await delete_pattern_cache("cache:titles:*")
        log.info(f"Title id={id} updated successfully")
        return {"id": title_id}

    @staticmethod
    async def delete_titles(title_ids: list[str]):
        log.info(f"Deleting titles: {title_ids}")
        await TitleRepository.delete_one_or_many(model_ids=title_ids)
        await delete_pattern_cache("cache:titles:*")
        log.info(f"Titles deleted successfully: {title_ids}")
