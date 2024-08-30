from pydantic import SecretStr
from pydantic_settings import BaseSettings
from sqlalchemy import URL


class BaseDatabaseConfig(BaseSettings):
    drivername: str
    username: str
    password: SecretStr
    host: str
    port: int
    database: str

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


if __name__ == "__main__":
    print(
        BaseDatabaseConfig(
            drivername="mysql", username="username", password="password", host="host", port=1, database="database"
        ).url
    )
