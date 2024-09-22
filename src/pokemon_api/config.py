from pydantic_settings import BaseSettings, SettingsConfigDict
from shared.database.config import BaseDatabaseConfig


class ServiceConfig(BaseSettings):
    database: BaseDatabaseConfig

    model_config = SettingsConfigDict(env_prefix="POKEMON_API_", env_nested_delimiter="__")
