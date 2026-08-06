from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product
from app.repositories import product_repository
from app.schemas.product_schema import CategoryCreate, ProductCreate
from app.utils.exceptions import NotFoundError


# ---------- Category ----------
def create_category(db: Session, data: CategoryCreate) -> Category:
    category = Category(name=data.name, description=data.description)
    return product_repository.create_category(db, category)


def get_category(db: Session, category_id: int) -> Category:
    category = product_repository.get_category(db, category_id)
    if category is None:
        raise NotFoundError("Category not found")
    return category


# ---------- Product ----------
def create_product(db: Session, data: ProductCreate) -> Product:
    # business rule: category must exist before adding a product to it
    if product_repository.get_category(db, data.category_id) is None:
        raise NotFoundError("Category not found")

    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        category_id=data.category_id,
    )
    return product_repository.create_product(db, product)


def get_product(db: Session, product_id: int) -> Product:
    product = product_repository.get_product(db, product_id)
    if product is None:
        raise NotFoundError("Product not found")
    return product


def list_products(db: Session) -> list[Product]:
    return product_repository.list_products(db)