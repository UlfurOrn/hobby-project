import pytest
import sqlalchemy
from shared.database.config import BaseDatabaseConfig
from shared.database.database import (
    close_database,
    get_db_engine,
    get_db_session,
    get_db_session_factory,
    init_database,
)
from shared.database.exceptions import DatabaseAlreadyInitializedError, DatabaseNotInitializedError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


@pytest.fixture
def config() -> BaseDatabaseConfig:
    return BaseDatabaseConfig(drivername="sqlite+aiosqlite")


@pytest.fixture
async def database(config):
    """Initialize a database connection and attempt to close it after running test"""
    init_database(config)
    yield

    try:
        await close_database()
    except DatabaseNotInitializedError:
        pass  # Database already closed


async def test_init_database(database):
    assert isinstance(get_db_engine(), AsyncEngine)
    assert isinstance(get_db_session_factory(), async_sessionmaker)
    assert isinstance(get_db_session(), AsyncSession)


async def test_get_db_engine(database):
    db_engine = get_db_engine()

    assert isinstance(db_engine, AsyncEngine)


async def test_get_db_session_factory(database):
    db_session_factory = get_db_session_factory()

    assert isinstance(db_session_factory, async_sessionmaker)
    assert isinstance(db_session_factory(), AsyncSession)


async def test_get_db_session(database):
    db_session = get_db_session()

    assert isinstance(db_session, AsyncSession)

    query = sqlalchemy.text("SELECT 1;")
    result = await db_session.execute(query)
    assert result.scalar() == 1


def test_init_database_twice(database, config):
    # Database already initialized once via database fixture
    with pytest.raises(DatabaseAlreadyInitializedError):
        init_database(config)


async def test_close_database(database):
    assert isinstance(get_db_engine(), AsyncEngine)

    await close_database()

    with pytest.raises(DatabaseNotInitializedError):
        get_db_engine()

    with pytest.raises(DatabaseNotInitializedError):
        get_db_session_factory()

    with pytest.raises(DatabaseNotInitializedError):
        get_db_session()


async def test_close_database_twice(database):
    await close_database()

    with pytest.raises(DatabaseNotInitializedError):
        await close_database()


async def test_use_without_initialization():
    with pytest.raises(DatabaseNotInitializedError):
        get_db_engine()

    with pytest.raises(DatabaseNotInitializedError):
        get_db_session_factory()

    with pytest.raises(DatabaseNotInitializedError):
        get_db_session()

    with pytest.raises(DatabaseNotInitializedError):
        await close_database()
