import sys

from loguru import logger


def init_logging() -> None:
    logger.remove(0)  # Remove the default loguru configuration

    logger.add(sys.stdout)
