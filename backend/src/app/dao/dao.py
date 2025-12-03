from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from .base_dao import BaseDAO
from ..models import Author, Publisher, Tag, Title, Genre, User
from ..db import connection


class AuthorDAO(BaseDAO[Author]):
    model = Author

    @classmethod
    @connection
    async def get_author_title(cls, session: AsyncSession, model_id: int | str):
        query = (
            select(cls.model)
            .options(selectinload(cls.model.titles))
            .filter_by(id=model_id)
        )
        result = await session.execute(query)
        info_one = result.scalar_one_or_none()
        return info_one


class PublisherDAO(BaseDAO[Publisher]):
    model = Publisher

    @classmethod
    @connection
    async def get_publisher_title(cls, session: AsyncSession, model_id: int | str):
        query = (
            select(cls.model)
            .options(selectinload(cls.model.titles))
            .filter_by(id=model_id)
        )
        result = await session.execute(query)
        info_one = result.scalar_one_or_none()
        return info_one


class TitleDAO(BaseDAO[Title]):
    model = Title

    @classmethod
    @connection
    async def get_all(
        cls,
        session: AsyncSession,
        type: str,
        status: str,
        release_format: str,
        genres: list[int],
        tags: list[int],
        page: int,
        limit: int,
    ):
        query = select(cls.model)

        if type:
            query = query.where(cls.model.type == type)

        if status:
            query = query.where(cls.model.status == status)

        if release_format:
            query = query.where(cls.model.release_format == release_format)

        if genres:
            query = query.where(cls.model.genres.any(Genre.id.in_(genres)))

        if tags:
            query = query.where(cls.model.tags.any(Tag.id.in_(tags)))

        query = query.offset((page - 1) * limit).limit(limit)
        result = await session.execute(query)
        info_all = result.scalars().all()
        return info_all

    @classmethod
    @connection
    async def get_by_id(cls, session: AsyncSession, model_id: int):
        query = (
            select(cls.model)
            .options(
                selectinload(cls.model.author),
                selectinload(cls.model.publisher),
                selectinload(cls.model.genres),
                selectinload(cls.model.tags),
            )
            .filter_by(id=model_id)
        )
        result = await session.execute(query)
        info_one = result.scalar_one_or_none()
        return info_one

    @classmethod
    @connection
    async def add(cls, session: AsyncSession, values: BaseModel):
        values = values.model_dump(exclude_unset=True)

        genre_ids = values.pop("genres", [])
        genres = await GenreDAO.get_by_ids(ids=genre_ids)

        tag_ids = values.pop("tags", [])
        tags = await TagDAO.get_by_ids(ids=tag_ids)

        author_id = values.pop("author_id")
        author = await AuthorDAO.get_by_id(model_id=author_id)

        publisher_id = values.pop("publisher_id")
        publisher = await PublisherDAO.get_by_id(model_id=publisher_id)

        new_title = cls.model(
            **values, author=author, publisher=publisher, genres=genres, tags=tags
        )
        session.add(new_title)
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        return new_title


class TagDAO(BaseDAO[Tag]):
    model = Tag


class GenreDAO(BaseDAO[Genre]):
    model = Genre


class UserDAO(BaseDAO[User]):
    model = User

    @classmethod
    @connection
    async def get_by_email(cls, session: AsyncSession, model_email: str):
        query = select(cls.model).filter_by(email=model_email)
        result = await session.execute(query)
        info_one = result.scalar_one_or_none()
        return info_one
