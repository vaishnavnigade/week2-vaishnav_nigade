from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.repositories import cart_repository, order_repository, user_repository
from app.utils.exceptions import NotFoundError, OutOfStockError


def create_order_from_cart(db: Session, user_id: int) -> Order:
    # validate user
    if user_repository.get_user(db, user_id) is None:
        raise NotFoundError("User not found")

    # cart must not be empty
    cart_items = cart_repository.list_cart_items(db, user_id)
    if not cart_items:
        raise NotFoundError("Cart is empty")

    order_items: list[OrderItem] = []
    total = Decimal("0.00")

    for item in cart_items:
        product = item.product
        if product.stock < item.quantity:
            raise OutOfStockError(f"Not enough stock for '{product.name}'")

        # freeze unit price and reduce stock
        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
            )
        )
        total += product.price * item.quantity
        product.stock -= item.quantity

    order = Order(
        user_id=user_id,
        status="pending",
        total_amount=total,
        items=order_items,
    )
    created = order_repository.create_order(db, order)

    # empty the cart after successful order
    for item in cart_items:
        cart_repository.delete_cart_item(db, item)

    return created


def get_order(db: Session, order_id: int) -> Order:
    order = order_repository.get_order(db, order_id)
    if order is None:
        raise NotFoundError("Order not found")
    return order


def list_orders(db: Session, user_id: int) -> list[Order]:
    return order_repository.list_orders(db, user_id)