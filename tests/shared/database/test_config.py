import pytest
from shared.database.config import BaseDatabaseConfig
from sqlalchemy import URL


@pytest.fixture
def config():
    return BaseDatabaseConfig(
        drivername="drivername",
        username="username",
        password="password",
        host="127.0.0.1",
        port=1234,
        database="database",
    )


def test_config_creates_valid_url(config):
    assert config.url == URL.create(
        drivername="drivername",
        username="username",
        password="password",
        host="127.0.0.1",
        port=1234,
        database="database",
    )


def test_config_hides_password_in_url(config):
    assert str(config.url) == "drivername://username:***@127.0.0.1:1234/database"


def test_config_also_supports_sqlite_like_connection_strings():
    config = BaseDatabaseConfig(drivername="sqlite")

    assert str(config.url) == "sqlite://"
