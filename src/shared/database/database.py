from typing import Callable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from shared.database.config import BaseDatabaseConfig

INIT_DATABASE = "Missing call to init_database"


_db_engine: AsyncEngine | None = None
_db_session_factory: Callable[..., AsyncSession] | None = None


def init_database(config: BaseDatabaseConfig) -> None:
    global _db_engine, _db_session_factory

    if _db_engine is not None:
        raise ValueError("init_database has already been called")

    _db_engine = create_async_engine(config.url, **config.engine_configuration_options)
    _db_session_factory = async_sessionmaker(_db_engine, **config.session_configuration_options)


async def close_database() -> None:
    global _db_engine, _db_session_factory

    if _db_engine is None:
        raise ValueError("Database connection was either never established or has already been closed")

    await _db_engine.dispose()

    _db_engine = None
    _db_session_factory = None


def get_db_engine() -> AsyncEngine:
    if _db_engine is None:
        raise ValueError(INIT_DATABASE)
    return _db_engine


def get_db_session_factory() -> Callable[..., AsyncSession]:
    if _db_session_factory is None:
        raise ValueError(INIT_DATABASE)
    return _db_session_factory


def get_db_session() -> AsyncSession:
    if _db_session_factory is None:
        raise ValueError(INIT_DATABASE)
    return _db_session_factory()
