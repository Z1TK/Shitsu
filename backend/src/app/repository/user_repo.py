from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.app.models.user import User
from backend.src.app.repository.base_repo import BaseRepository
from backend.src.app.utils.decorators import connection


class UserRepository(BaseRepository[User]):
    model = User

    @classmethod
    @connection(commit=False)
    async def get_by_email(cls, session: AsyncSession, model_email: str):
        stmt = select(cls.model).where(cls.model.email == model_email)
        obj = await session.execute(stmt)
        return obj.scalar_one_or_none()
