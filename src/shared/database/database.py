from typing import Callable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from shared.database.config import BaseDatabaseConfig

_db_engine: AsyncEngine | None = None
_db_session_factory: Callable[..., AsyncSession] | None = None


def init_database(config: BaseDatabaseConfig) -> None:
    engine = create_async_engine(config.url)

    set_db_engine(engine)

    # session = async_sessionmaker(engine)


def set_db_engine(engine: AsyncEngine) -> None:
    global _db_engine, _db_session_factory

    _db_engine = engine
    _db_session_factory = async_sessionmaker(engine, expire_on_commit=False)


def get_db_engine() -> AsyncEngine:
    global _db_engine

    if not _db_engine:
        raise ValueError("Must call init_database")

    return _db_engine


if __name__ == "__main__":

    class ThisModel(DeclarativeBase):
        pass

    class OtherModel(DeclarativeBase):
        pass

    class ThirdModel(DeclarativeBase):
        pass

    config = BaseDatabaseConfig(
        drivername="mysql",
        username="username",
        password="password",
        host="host",
        port=1,
        database="database",
        base_model=ThisModel,
    )

    init_database(config)

    other_config = config.__deepcopy__()
    other_config.base_model = OtherModel

    init_database(other_config)

    print(get_db_engine(ThisModel))
    print(get_db_engine(OtherModel))
    print(get_db_engine(ThirdModel))
