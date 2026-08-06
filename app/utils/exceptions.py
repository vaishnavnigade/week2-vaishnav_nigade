class NotFoundError(Exception):
    """Raised when a requested record does not exist."""
    pass


class AlreadyExistsError(Exception):
    """Raised when a record already exists (e.g. duplicate email)."""
    pass


class InvalidCredentialsError(Exception):
    """Raised when login email/password is wrong."""
    pass


class OutOfStockError(Exception):
    """Raised when a product does not have enough stock."""
    pass