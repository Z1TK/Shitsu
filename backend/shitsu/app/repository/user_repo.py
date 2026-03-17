from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.shitsu.app.models.user import User
from backend.shitsu.app.repository.base_repo import BaseRepository
from backend.shitsu.app.utils.decorators import connection


class UserRepository(BaseRepository[User]):
    model = User

    @classmethod
    @connection(commit=False)
    async def get_by_email(cls, model_email: str, session: AsyncSession):
        stmt = (
            select(cls.model)
            .options(selectinload(cls.model.comments))
            .where(cls.model.email == model_email)
        )
        obj = await session.execute(stmt)
        return obj.scalar_one_or_none()
    
    @classmethod
    @connection()
    async def update_by_email(cls, session: AsyncSession, model_email: str, **kwargs):
        stmt = (
            update(cls.model)
            .where(cls.model.email == model_email)
            .values(**kwargs)
            .returning(cls.model)
        )
        obj = await session.execute(stmt)
        await session.flush()
        return obj.scalar_one_or_none()
