class NotFoundError(Exception):
    """Raised when a requested record does not exist."""
    pass


class AlreadyExistsError(Exception):
    """Raised when creating a record that violates uniqueness."""
    pass


class OutOfStockError(Exception):
    """Raised when a product does not have enough stock."""
    pass