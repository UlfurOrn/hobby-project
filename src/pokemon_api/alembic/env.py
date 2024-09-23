import asyncio

from alembic import context
from dotenv import load_dotenv
from pokemon_api.config import DatabaseConfig
from pokemon_api.models.pokemon import BaseDB
from shared.database.config import BaseDatabaseConfig
from shared.database.database import close_database, get_db_engine, init_database
from sqlalchemy import NullPool
from sqlalchemy.engine import Connection


async def main():
    load_dotenv()
    config = DatabaseConfig()

    if context.is_offline_mode():
        run_migrations_offline(config)
    else:
        await run_migrations_online(config)


def run_migrations_offline(config: BaseDatabaseConfig) -> None:
    """Run migrations in 'offline' mode.

    This is done by providing the --sql flag to various alembic commands.

    This does not require a connection to a database. Instead, it dumps the SQL commands, that it would normally
    execute against the database, to the console.
    """
    context.configure(
        url=config.url,
        target_metadata=BaseDB.metadata,
        # Additional Configuration to turn WHERE name=$1::VARCHAR into WHERE name="Charizard"
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online(config: BaseDatabaseConfig) -> None:
    """Run migrations in 'online' mode.

    This is the default when using alembic commands.

    This requires a connection to a database. It executes the SQL commands defined in the alembic revision files
    against the database.
    """
    init_database(config, poolclass=NullPool)

    engine = get_db_engine()

    async with engine.connect() as connection:
        # Alembic requires a synchronous engine and execution for its migrations
        await connection.run_sync(run_migration_synchronously)

    await close_database()


def run_migration_synchronously(connection: Connection) -> None:
    """Migrate the database associated with the given connection."""
    context.configure(connection=connection, target_metadata=BaseDB.metadata)

    with context.begin_transaction():
        context.run_migrations()


asyncio.run(main())
