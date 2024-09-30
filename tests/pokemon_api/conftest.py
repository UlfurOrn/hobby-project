import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from pokemon_api.config import DatabaseConfig
from pokemon_api.main import app
from pokemon_api.models.pokemon import BaseDB
from shared.database.database import close_database, get_db_engine, get_db_session, init_database
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

### Database ###


@pytest.fixture(scope="session")
def database_config() -> DatabaseConfig:
    return DatabaseConfig(
        drivername="sqlite+aiosqlite",
        username=None,
        password=None,
        host=None,
        port=None,
        database=None,
    )


@pytest.fixture(scope="session")
async def database(database_config):
    """Initialize a database connection for the test run."""

    init_database(database_config)

    db_engine = get_db_engine()
    async with db_engine.begin() as conn:
        # Tear down any existing data in the database then recreate the tables
        await conn.run_sync(BaseDB.metadata.drop_all)
        await conn.run_sync(BaseDB.metadata.create_all)

    yield

    await close_database()


@pytest.fixture(scope="function")
async def clean_database(database):
    """Remove all data from the database before a test case."""

    async with get_db_session() as session:
        # We use reversed so that tables that we don't get foreign key errors
        for table in reversed(BaseDB.metadata.sorted_tables):
            delete_data_in_table_query = delete(table)
            await session.execute(delete_data_in_table_query)

        await session.commit()


@pytest.fixture(scope="function")
async def db_session(clean_database) -> AsyncSession:
    with get_db_session() as session:
        yield session


### API ###


@pytest.fixture
def api(clean_database) -> FastAPI:
    return app


@pytest.fixture
async def api_client(api) -> AsyncClient:
    async with AsyncClient(app=api, base_url="http://testserver") as test_client:
        yield test_client
