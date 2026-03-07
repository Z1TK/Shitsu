from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.shitsu.app.models.publisher import Publisher
from backend.shitsu.app.repository.base_repo import BaseRepository
from backend.shitsu.app.utils.decorators import connection


class PublisherRepository(BaseRepository[Publisher]):
    model = Publisher

    @classmethod
    @connection(commit=False)
    async def get_publisher_title(cls, model_id: int | str, session: AsyncSession):
        stmt = (
            select(cls.model)
            .options(selectinload(cls.model.titles))
            .where(cls.model.id == model_id)
        )
        obj = await session.execute(stmt)
        return obj.scalar_one_or_none()
