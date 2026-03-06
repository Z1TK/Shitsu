from fastapi import HTTPException

from backend.shitsu.app.repository.author_repo import AuthorRepository
from backend.shitsu.app.schemas.author import (
    AuthorCreateSchema,
    AuthorIdSchema,
    AuthorReadSchema,
    AuthorUpdateSchema,
)
from backend.shitsu.app.logger import log


class AuthorService:

    from backend.shitsu.app.logger import log


class AuthorService:

    @staticmethod
    async def get_all_authors(page: int, limit: int):
        log.info(f"Fetching all authors: page={page}, limit={limit}")
        authors = await AuthorRepository.get_all(page=page, limit=limit)
        if not authors:
            log.warning("No authors found")
            raise HTTPException(status_code=404, detail="Authors not found")
        log.info(f"Found {len(authors)} authors")
        return [
            AuthorReadSchema.model_validate(author).model_dump() for author in authors
        ]

    @staticmethod
    async def get_author_by_id(author_id: str):
        log.info(f"Fetching author by id={author_id}")
        author = await AuthorRepository.get_by_id(model_id=author_id)
        if not author:
            log.warning(f"Author id={author_id} not found")
            raise HTTPException(status_code=404, detail="Author not found")
        log.info(f"Found author id={author_id}")
        return AuthorIdSchema.model_validate(author).model_dump()

    @staticmethod
    async def add_author(dto: AuthorCreateSchema):
        log.info(f"Creating author: {dto.model_dump()}")
        value = dto.model_dump()
        author = await AuthorRepository.add(**value)
        if not author:
            log.error("Failed to create author")
            raise HTTPException(status_code=400, detail="Failed to create author")
        log.info(f"Author created successfully")
        return AuthorReadSchema.model_validate(author).model_dump()

    @staticmethod
    async def update_author(author_id: str, dto: AuthorUpdateSchema):
        log.info(
            f"Updating author id={author_id}: {dto.model_dump(exclude_unset=True)}"
        )
        value = dto.model_dump(exclude_unset=True)
        author = await AuthorRepository.update_by_id(model_id=author_id, **value)
        if not author:
            log.warning(f"Author id={author_id} not found for update")
            raise HTTPException(status_code=404, detail="Author not found")
        log.info(f"Author id={author_id} updated successfully")
        return AuthorReadSchema.model_validate(author).model_dump()

    @staticmethod
    async def delete_authors(author_ids: list[str]):
        log.info(f"Deleting authors: {author_ids}")
        await AuthorRepository.delete_one_or_many(model_ids=author_ids)
        log.info(f"Authors deleted successfully: {author_ids}")
