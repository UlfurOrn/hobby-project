from pydantic_settings import BaseSettings, SettingsConfigDict
from shared.database.config import BaseDatabaseConfig


class DatabaseConfig(BaseDatabaseConfig):
    """Subclass the BaseDatabaseConfig class to provide some defaults for the Pokemon API Database"""

    drivername: str = "postgresql+asyncpg"
    database: str = "pokemon"

    # Provide the env_prefix here so this config object can be loaded individually for DB migrations etc.
    model_config = SettingsConfigDict(env_prefix="POKEMON_API_DATABASE__")


class ServiceConfig(BaseSettings):
    database: DatabaseConfig

    model_config = SettingsConfigDict(env_prefix="POKEMON_API_", env_nested_delimiter="__")
