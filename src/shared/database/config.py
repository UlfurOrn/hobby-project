from typing import Any

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings
from sqlalchemy import URL


class BaseDatabaseConfig(BaseSettings):
    drivername: str
    username: str
    password: SecretStr
    host: str
    port: int
    database: str

    # Available Options: https://docs.sqlalchemy.org/en/20/core/engines.html#
    engine_configuration_options: dict[str, Any] = Field(default_factory=dict)
    # Available Options: https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session
    session_configuration_options: dict[str, Any] = Field(default_factory=dict)

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.drivername,
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.database,
        )
