
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class that all SQLAlchemy ORM models inherit from."""
    pass


# ---------------------------------------------------------------------------
# Import every model here so its table registers on Base.metadata.
# This is required for Base.metadata.create_all() and Alembic to "see" them.
# Keep these imports AFTER Base is defined to avoid circular-import errors.
# Uncomment each line as soon as you create that model file in Step 3.
# ---------------------------------------------------------------------------
# from app.models.user import User          # noqa: E402,F401
# from app.models.category import Category   # noqa: E402,F401
# from app.models.product import Product     # noqa: E402,F401
# from app.models.cart import Cart           # noqa: E402,F401
# from app.models.order import Order         # noqa: E402,F401
