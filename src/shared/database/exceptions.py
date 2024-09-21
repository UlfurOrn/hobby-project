class DatabaseNotInitializedError(Exception):
    """Exception raised when the database has not been initialized."""


class DatabaseAlreadyInitializedError(Exception):
    """Exception raised when the database has already been initialized."""
