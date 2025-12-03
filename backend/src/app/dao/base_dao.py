from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from pydantic import BaseModel
from fastapi import HTTPException
from uuid import UUID

from ..db import connection
from ..db import Base


class BaseDAO[T: Base]:
    model: type[T]

    @classmethod
    @connection
    async def get_all(cls, session: AsyncSession, page: int, limit: int):
        query = select(cls.model).offset((page - 1) * limit).limit(limit)
        result = await session.execute(query)
        info_all = result.scalars().all()
        return info_all

    @classmethod
    @connection
    async def get_by_id(cls, session: AsyncSession, model_id: int | str):
        query = select(cls.model).filter_by(id=model_id)
        result = await session.execute(query)
        info_one = result.scalar_one_or_none()
        return info_one

    @classmethod
    @connection
    async def get_by_ids(cls, session: AsyncSession, ids: list[int]):
        query = select(cls.model).where(cls.model.id.in_(ids))
        result = await session.execute(query)
        ids = result.scalars().all()
        return ids

    @classmethod
    @connection
    async def add(cls, session: AsyncSession, values: BaseModel):
        values = values.model_dump(exclude_unset=True)
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
            await session.refresh(new_instance)
        except Exception as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    @connection
    async def update_by_id(
        cls, session: AsyncSession, values: BaseModel, model_id: int | str
    ):
        values = values.model_dump(exclude_unset=True)
        stmt = (
            update(cls.model)
            .filter_by(id=model_id)
            .values(**values)
            .returning(cls.model)
        )
        try:
            result = await session.execute(stmt)
            await session.commit()
            update_instance = result.scalar_one_or_none()
            return update_instance
        except Exception as e:
            await session.rollback()
            raise e

    @classmethod
    @connection
    async def delete_one_or_many(
        cls, session: AsyncSession, model_ids: list[int | str]
    ):
        query = select(cls.model.id).where(cls.model.id.in_(model_ids))
        result = await session.execute(query)
        existing_ids = result.scalars().all()

        missing_ids = len(model_ids) - len(existing_ids)
        if missing_ids:
            raise HTTPException(status_code=404, detail={"error": f"Not found ID/IDs"})

        query = delete(cls.model).where(cls.model.id.in_(existing_ids))
        try:
            await session.execute(query)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
