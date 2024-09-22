from typing import Callable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from shared.database.config import BaseDatabaseConfig

DATABASE_NOT_INITIALIZED = "A database connection has not been established"
DATABASE_ALREADY_INITIALIZED = "A database connection has already been established"


_db_engine: AsyncEngine | None = None
_db_session_factory: Callable[..., AsyncSession] | None = None


def get_db_engine() -> AsyncEngine:
    if _db_engine is None:
        raise RuntimeError(DATABASE_NOT_INITIALIZED)
    return _db_engine


def get_db_session_factory() -> Callable[..., AsyncSession]:
    if _db_engine is None:
        raise RuntimeError(DATABASE_NOT_INITIALIZED)
    return _db_session_factory


def get_db_session(**session_configuration_option_overrides) -> AsyncSession:
    if _db_engine is None:
        raise RuntimeError(DATABASE_NOT_INITIALIZED)
    return _db_session_factory(**session_configuration_option_overrides)


def init_database(config: BaseDatabaseConfig) -> None:
    global _db_engine, _db_session_factory

    if _db_engine is not None:
        raise RuntimeError(DATABASE_ALREADY_INITIALIZED)

    _db_engine = create_async_engine(config.url, **config.engine_configuration_options)
    _db_session_factory = async_sessionmaker(_db_engine, **config.session_configuration_options)


async def close_database() -> None:
    global _db_engine, _db_session_factory

    if _db_engine is None:
        raise RuntimeError(DATABASE_NOT_INITIALIZED)

    await _db_engine.dispose()

    _db_engine = None
    _db_session_factory = None
