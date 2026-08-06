from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.category import Category
from app.models.product import Product


# ---------- Category ----------
def create_category(db: Session, category: Category) -> Category:
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_category(db: Session, category_id: int) -> Category | None:
    # eager-load products (same idea as selectinload(Department.employees))
    statement = (
        select(Category)
        .options(selectinload(Category.products))
        .where(Category.id == category_id)
    )
    return db.scalar(statement)


# ---------- Product ----------
def create_product(db: Session, product: Product) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def list_products(db: Session) -> list[Product]:
    return list(db.scalars(select(Product)))


def update_stock(db: Session, product: Product, new_stock: int) -> Product:
    product.stock = new_stock
    db.commit()
    db.refresh(product)
    return product