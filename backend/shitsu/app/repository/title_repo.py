from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.shitsu.app.models.genre import Genre
from backend.shitsu.app.models.tag import Tag
from backend.shitsu.app.models.title import Title
from backend.shitsu.app.repository.base_repo import BaseRepository
from backend.shitsu.app.utils.decorators import connection


class TitleRepository(BaseRepository[Title]):
    model = Title

    @classmethod
    @connection(commit=False)
    async def get_all(
        cls,
        type: str,
        status: str,
        release_format: str,
        genres: list[int],
        tags: list[int],
        page: int,
        limit: int,
        session: AsyncSession
    ):
        stmt = select(cls.model)

        if type:
            stmt = stmt.where(cls.model.type == type)

        if status:
            stmt = stmt.where(cls.model.status == status)

        if release_format:
            stmt = stmt.where(cls.model.release_format == release_format)

        if genres:
            stmt = stmt.where(cls.model.genres.any(Genre.id.in_(genres)))

        if tags:
            stmt = stmt.where(cls.model.tags.any(Tag.id.in_(tags)))

        stmt = stmt.offset((page - 1) * limit).limit(limit)
        obj = await session.execute(stmt)
        return obj.scalars().all()

    @classmethod
    @connection(commit=False)
    async def get_by_id(cls, model_id: int, session: AsyncSession):
        stmt = (
            select(cls.model)
            .options(
                selectinload(cls.model.author),
                selectinload(cls.model.publisher),
                selectinload(cls.model.genres),
                selectinload(cls.model.tags),
            )
            .where(cls.model.id == model_id)
        )
        obj = await session.execute(stmt)
        return obj.scalar_one_or_none()

    @classmethod
    @connection()
    async def create(cls, session: AsyncSession, **kwargs):
        obj = cls.model(**kwargs)
        session.add(obj)
        await session.flush()
        await session.refresh(obj)
        return obj.id

    @classmethod
    @connection()
    async def update_by_id(cls, session: AsyncSession, model_id: int | str, **kwargs):
        stmt = (
            update(cls.model)
            .where(cls.model.id == model_id)
            .values(**kwargs)
            .returning(cls.model.id)
        )
        obj = await session.execute(stmt)
        await session.flush()
        return obj.scalar_one()
