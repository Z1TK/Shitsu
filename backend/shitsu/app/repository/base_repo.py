from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.shitsu.app.models.base_mode import Base
from backend.shitsu.app.utils.decorators import connection


class BaseRepository[T: Base]:
    model: type[T]

    @classmethod
    @connection(commit=False)
    async def get_all(cls, page: int, limit: int, session: AsyncSession,):
        stmt = select(cls.model).offset((page - 1) * limit).limit(limit)
        obj = await session.execute(stmt)
        return obj.scalars().all()

    @classmethod
    @connection(commit=False)
    async def get_by_id(cls, model_id: int | str, session: AsyncSession):
        stmt = select(cls.model).where(cls.model.id == model_id)
        obj = await session.execute(stmt)
        return obj.scalar_one_or_none()

    @classmethod
    @connection(commit=False)
    async def get_by_ids(cls, ids: list[int], session: AsyncSession):
        stmt = select(cls.model).where(cls.model.id.in_(ids))
        obj = await session.execute(stmt)
        return obj.scalars().all()

    @classmethod
    @connection()
    async def add(cls, session: AsyncSession, **kwargs):
        obj = cls.model(**kwargs)
        session.add(obj)
        await session.flush()
        await session.refresh(obj)
        return obj

    @classmethod
    @connection()
    async def update_by_id(cls, session: AsyncSession, model_id: int | str, **kwargs):
        stmt = (
            update(cls.model)
            .where(cls.model.id == model_id)
            .values(**kwargs)
            .returning(cls.model)
        )
        obj = await session.execute(stmt)
        await session.flush()
        return obj.scalar_one_or_none()

    @classmethod
    @connection()
    async def delete_one_or_many(
        cls, session: AsyncSession, model_ids: list[int | str]
    ):
        stmt = select(cls.model.id).where(cls.model.id.in_(model_ids))
        obj = await session.execute(stmt)
        existing_ids = obj.scalars().all()
        # missing_ids = len(model_ids) - len(existing_ids)
        stmt = delete(cls.model).where(cls.model.id.in_(existing_ids))
        await session.execute(stmt)
        await session.flush()
