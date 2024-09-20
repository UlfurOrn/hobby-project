from typing import Callable

import pytest
from shared.database.config import BaseDatabaseConfig
from shared.database.database import (
    close_database,
    get_db_engine,
    get_db_session,
    get_db_session_factory,
    init_database,
)
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


@pytest.fixture
def database_config():
    return BaseDatabaseConfig(drivername="sqlite+aiosqlite")


@pytest.mark.asyncio
async def test_init_database(database_config):
    try:
        init_database(database_config)

        assert isinstance(get_db_engine(), AsyncEngine)
        assert isinstance(get_db_session_factory(), Callable)
        assert isinstance(get_db_session_factory()(), AsyncSession)
        assert isinstance(get_db_session(), AsyncSession)
    except AssertionError:
        raise
    finally:
        await close_database()
