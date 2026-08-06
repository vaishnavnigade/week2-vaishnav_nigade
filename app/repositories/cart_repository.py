from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.cart import CartItem


def add_cart_item(db: Session, cart_item: CartItem) -> CartItem:
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


def get_cart_item(db: Session, cart_item_id: int) -> CartItem | None:
    return db.get(CartItem, cart_item_id)


def get_cart_item_by_product(db: Session, user_id: int, product_id: int) -> CartItem | None:
    statement = select(CartItem).where(
        CartItem.user_id == user_id, CartItem.product_id == product_id
    )
    return db.scalar(statement)


def list_cart_items(db: Session, user_id: int) -> list[CartItem]:
    # eager-load the product so the response has product details
    statement = (
        select(CartItem)
        .options(selectinload(CartItem.product))
        .where(CartItem.user_id == user_id)
    )
    return list(db.scalars(statement))


def update_cart_item(db: Session, cart_item: CartItem, quantity: int) -> CartItem:
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


def delete_cart_item(db: Session, cart_item: CartItem) -> None:
    db.delete(cart_item)
    db.commit()