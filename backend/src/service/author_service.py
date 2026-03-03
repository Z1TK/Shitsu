from fastapi import HTTPException

from backend.src.app.repository.author_repo import AuthorRepository
from backend.src.app.schemas.author import (AuthorCreateSchema, AuthorIdSchema,
                                            AuthorReadSchema,
                                            AuthorUpdateSchema)


class AuthorService:

    @staticmethod
    async def get_all_authors(page: int, limit: int):
        authors = await AuthorRepository.get_all(page=page, limit=limit)
        if not authors:
            raise HTTPException(status_code=404, detail="Authors not found")
        return [
            AuthorReadSchema.model_validate(author).model_dump() for author in authors
        ]

    @staticmethod
    async def get_author_by_id(author_id: str):
        author = await AuthorRepository.get_by_id(model_id=author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return AuthorIdSchema.model_validate(author).model_dump()

    @staticmethod
    async def add_author(dto: AuthorCreateSchema):
        value = dto.model_dump()
        author = await AuthorRepository.add(**value)
        if not author:
            raise HTTPException(status_code=400, detail="Failed to create author")
        return AuthorReadSchema.model_validate(author).model_dump()

    @staticmethod
    async def update_author(author_id: str, dto: AuthorUpdateSchema):
        value = dto.model_dump(exclude_unset=True)
        author = await AuthorRepository.update_by_id(model_id=author_id, **value)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return AuthorReadSchema.model_validate(author).model_dump()

    @staticmethod
    async def delete_authors(author_ids: list[str]):
        await AuthorRepository.delete_one_or_many(model_ids=author_ids)
