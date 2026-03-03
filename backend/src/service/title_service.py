from fastapi import HTTPException

from backend.src.app.repository.title_repo import TitleRepository
from backend.src.app.schemas.title import (TitleCreateSchema,
                                           TitleReadAllSchema,
                                           TitleReadIDSchema,
                                           TitleUpdateSchema)


class TitleService:

    @staticmethod
    async def get_all_titles(
        page: int,
        limit: int,
        type: str,
        status: str,
        release_format: str,
        genres: list[int],
        tags: list[int],
    ):
        titles = await TitleRepository.get_all(
            page=page,
            limit=limit,
            type=type,
            status=status,
            release_format=release_format,
            genres=genres,
            tags=tags,
        )
        if not titles:
            raise HTTPException(status_code=404, detail="Titles not found")
        return [
            TitleReadAllSchema.model_validate(title).model_dump() for title in titles
        ]

    @staticmethod
    async def get_title_by_id(title_id: str):
        title = await TitleRepository.get_by_id(model_id=title_id)
        if not title:
            raise HTTPException(status_code=404, detail="Title not found")
        return TitleReadIDSchema.model_validate(title).model_dump()

    # @staticmethod
    # async def add_title(dto: TitleCreateSchema):
    #     value = dto.model_dump()
    #     title = await TitleRepository.add(**value)
    #     if not title:
    #         raise HTTPException(status_code=400, detail="Failed to create title")
    #     return TitleReadIDSchema.model_validate(title).model_dump()

    @staticmethod
    async def update_title(title_id: str, dto: TitleUpdateSchema):
        value = dto.model_dump(exclude_unset=True)
        title = await TitleRepository.update_by_id(model_id=title_id, **value)
        if not title:
            raise HTTPException(status_code=404, detail="Title not found")
        return TitleReadIDSchema.model_validate(title).model_dump()

    @staticmethod
    async def delete_titles(title_ids: list[str]):
        await TitleRepository.delete_one_or_many(model_ids=title_ids)
