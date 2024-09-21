from typing import Callable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from shared.database.config import BaseDatabaseConfig
from shared.database.exceptions import DatabaseNotInitializedError, DatabaseAlreadyInitializedError


class DatabaseSingleton:
    _db_engine: AsyncEngine | None = None
    _db_session_factory: Callable[..., AsyncSession] | None = None

    @classmethod
    def get_engine(cls) -> AsyncEngine:
        if cls._db_engine is None:
            raise DatabaseNotInitializedError()
        return cls._db_engine

    @classmethod
    def get_db_session_factory(cls) -> Callable[..., AsyncSession]:
        if cls._db_engine is None:
            raise DatabaseNotInitializedError()
        return cls._db_session_factory

    @classmethod
    def get_db_session(cls, **session_configuration_options) -> AsyncSession:
        if cls._db_engine is None:
            raise DatabaseNotInitializedError()
        return cls._db_session_factory(**session_configuration_options)

    @classmethod
    def init_database(cls, config: BaseDatabaseConfig) -> None:
        if cls._db_engine is not None:
            raise DatabaseAlreadyInitializedError()

        cls._db_engine = create_async_engine(config.url, **config.engine_configuration_options)
        cls._db_session_factory = async_sessionmaker(cls._db_engine, **config.session_configuration_options)

    @classmethod
    async def close_database(cls) -> None:
        if cls._db_engine is None:
            raise DatabaseNotInitializedError()

        await cls._db_engine.dispose()

        cls._db_engine = None
        cls._db_session_factory = None


def get_db_engine() -> AsyncEngine:
    return DatabaseSingleton.get_engine()


def get_db_session_factory() -> Callable[..., AsyncSession]:
    return DatabaseSingleton.get_db_session_factory()


def get_db_session(**session_configuration_options) -> AsyncSession:
    return DatabaseSingleton.get_db_session(**session_configuration_options)


def init_database(config: BaseDatabaseConfig) -> None:
    DatabaseSingleton.init_database(config)


async def close_database() -> None:
    await DatabaseSingleton.close_database()
