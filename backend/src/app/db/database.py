from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from functools import wraps

from ...core import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(DATABASE_URL)

async_session_marker = async_sessionmaker(engine, expire_on_commit=False)


def connection(method):
    @wraps(method)
    async def wrapper(*args, **kwargs):
        async with async_session_marker() as session:
            try:
                return await method(*args, **kwargs, session=session)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper
