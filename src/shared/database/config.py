from typing import Any

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings
from sqlalchemy import URL


class BaseDatabaseConfig(BaseSettings):
    drivername: str
    username: str | None = None
    password: SecretStr | None = None
    host: str | None = None
    port: int | None = None
    database: str | None = None

    # Available Options: https://docs.sqlalchemy.org/en/20/core/engines.html#
    engine_configuration_options: dict[str, Any] = Field(default_factory=dict)
    # Available Options: https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session
    session_configuration_options: dict[str, Any] = Field(default_factory=dict)

    @property
    def url(self) -> URL:
        password = None
        if isinstance(self.password, SecretStr):
            password = self.password.get_secret_value()

        return URL.create(
            drivername=self.drivername,
            username=self.username,
            password=password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
