import asyncio
from typing import Generator

import pytest


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
