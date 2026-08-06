# DeclarativeBase is SQLAlchemy's base class for defining ORM models declaratively.
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class inherited by all SQLAlchemy ORM models."""

    # No custom behavior needed; models inherit the shared metadata from this class.
    pass


# Import all models here so that defining them registers their tables on Base.metadata.
# This guarantees create_all() / migrations can see every table.
# (# noqa suppresses linter warnings: E402 = import not at top, F401 = imported but unused.)
from app.models.cart import CartItem  # noqa: E402,F401
from app.models.category import Category  # noqa: E402,F401
from app.models.order import Order, OrderItem # noqa: E402,F401
from app.models.product import Product  # noqa: E402,F401
from app.models.user import User  # noqa: E402,F401