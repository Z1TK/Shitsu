from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.shitsu.app.models.user import User
from backend.shitsu.app.repository.base_repo import BaseRepository
from backend.shitsu.app.utils.decorators import connection


class UserRepository(BaseRepository[User]):
    model = User

    @classmethod
    @connection(commit=False)
    async def get_by_id(cls, model_id: str, session: AsyncSession):
        stmt = (
            select(cls.model)
            .options(selectinload(cls.model.comments))
            .where(cls.model.id == model_id)
        )
        obj = await session.execute(stmt)
        return obj.scalar_one_or_none()
