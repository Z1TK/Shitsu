from fastapi import HTTPException

from backend.src.app.repository.tag_genre_repo import (GenreRepository,
                                                       TagRepository)
from backend.src.app.schemas.genre import GenreReadSchema
from backend.src.app.schemas.tag import TagReadSchema


class GenreService:

    @staticmethod
    async def get_all_genres(page: int, limit: int):
        authors = await GenreRepository.get_all(page=page, limit=limit)
        if not authors:
            raise HTTPException(status_code=404, detail="Authors not found")
        return [
            GenreReadSchema.model_validate(author).model_dump() for author in authors
        ]


class TagService:

    @staticmethod
    async def get_all_tags(page: int, limit: int):
        authors = await TagRepository.get_all(page=page, limit=limit)
        if not authors:
            raise HTTPException(status_code=404, detail="Authors not found")
        return [TagReadSchema.model_validate(author).model_dump() for author in authors]
