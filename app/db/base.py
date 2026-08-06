from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class inherited by all SQLAlchemy ORM models."""

    pass


# Import all models so their tables register with Base.metadata.
from app.models.cart import CartItem  # noqa: E402,F401
from app.models.category import Category  # noqa: E402,F401
from app.models.order import Order, OrderItem # noqa: E402,F401
from app.models.product import Product  # noqa: E402,F401
from app.models.user import User  # noqa: E402,F401