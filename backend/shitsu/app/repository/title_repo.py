from sqlalchemy import select, update, and_
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
        page: int,
        limit: int,
        type: list[str],
        status: list[str],
        release_format: list[str],
        genres: list[int],
        tags: list[int],
        year_min: int,
        year_max: int,
        # sort_by: str,
        genres_soft_search: bool,
        tags_soft_search: bool,
        session: AsyncSession,
    ):
        stmt = select(cls.model)

        if type:
            stmt = stmt.where(cls.model.type.in_(type))

        if status:
            stmt = stmt.where(cls.model.status.in_(status))

        if release_format:
            stmt = stmt.where(cls.model.release_format.in_(release_format))

        if genres_soft_search and genres:
            stmt = stmt.where(cls.model.genres.any(Genre.id.in_(genres)))
        elif genres:
            stmt = stmt.where(
                and_(*[cls.model.genres.any(Genre.id == genre) for genre in genres])
            )

        if tags_soft_search and tags:
            stmt = stmt.where(cls.model.tags.any(Tag.id.in_(tags)))
        elif tags:
            stmt = stmt.where(
                and_(*[cls.model.tags.any(Tag.id == tag) for tag in tags])
            )

        if year_min:
            stmt = stmt.where(cls.model.release_year >= year_min)

        if year_max:
            stmt = stmt.where(cls.model.release_year <= year_max)

        stmt = stmt.offset((page - 1) * limit).limit(limit)
        obj = await session.execute(stmt)
        return obj.scalars().all()

    @classmethod
    @connection(commit=False)
    async def get_by_id(cls, model_id: int, section: str, session: AsyncSession):
        stmt = select(cls.model).where(cls.model.id == model_id)
        if section == "info":
            stmt = stmt.options(
                selectinload(cls.model.author),
                selectinload(cls.model.publisher),
                selectinload(cls.model.genres),
                selectinload(cls.model.tags),
            )
        if section == "chapters":
            stmt = stmt.options(selectinload(cls.model.chapters))
        if section == "comments":
            stmt = stmt.opntions(selectinload(cls.model.comments))
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
