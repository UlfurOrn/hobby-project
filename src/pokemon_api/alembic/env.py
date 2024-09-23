import asyncio
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from pokemon_api.config import DatabaseConfig
from pokemon_api.models.pokemon import BaseDB
from shared.database.database import close_database, get_db_engine, init_database
from sqlalchemy import NullPool
from sqlalchemy.engine import Connection

target_metadata = BaseDB.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    load_dotenv()
    database_config = DatabaseConfig()

    context.configure(
        url=database_config.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    load_dotenv()
    database_config = DatabaseConfig()

    init_database(database_config, poolclass=NullPool, logging_name="alembic")

    engine = get_db_engine()

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await close_database()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
