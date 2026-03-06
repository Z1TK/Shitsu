from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.shitsu.app.models.author import Author
from backend.shitsu.app.repository.base_repo import BaseRepository
from backend.shitsu.app.utils.decorators import connection


class AuthorRepository(BaseRepository[Author]):
    model = Author

    @classmethod
    @connection(commit=False)
    async def get_by_id(cls, session: AsyncSession, model_id: int | str):
        stmt = (
            select(cls.model)
            .options(selectinload(cls.model.titles))
            .where(cls.model.id == model_id)
        )
        obj = await session.execute(stmt)
        return obj.scalar_one_or_none()
