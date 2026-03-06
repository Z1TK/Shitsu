from functools import wraps

from sqlalchemy.exc import DataError, IntegrityError, NoResultFound, OperationalError

from backend.shitsu.app.db.database import async_session_marker
from backend.shitsu.app.logger import log


def connection(commit: bool = True):
    def decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            async with async_session_marker() as session:
                try:
                    func = await method(*args, **kwargs, session=session)
                    if commit:
                        await session.commit()
                    return func
                except IntegrityError as e:
                    await session.rollback()
                    log.error("IntegrityError in %s: %s", func.__name__, e)
                    raise
                except OperationalError as e:
                    await session.rollback()
                    log.error("OperationalError in %s: %s", func.__name__, e)
                    raise
                except DataError as e:
                    await session.rollback()
                    log.error("DataError in %s: %s", func.__name__, e)
                    raise
                except NoResultFound as e:
                    await session.rollback()
                    log.error("NoResultFound in %s: %s", func.__name__, e)
                    raise
                finally:
                    await session.close()

        return wrapper

    return decorator
