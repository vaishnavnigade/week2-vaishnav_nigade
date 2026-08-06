from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class that all SQLAlchemy ORM models inherit from."""
    pass


# Import all models here so their tables register with Base.metadata
from app.models.user import User          # noqa: E402,F401
from app.models.category import Category  # noqa: E402,F401
from app.models.product import Product    # noqa: E402,F401
from app.models.cart import CartItem      # noqa: E402,F401