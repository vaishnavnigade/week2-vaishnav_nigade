from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.cart_schema import CartItemCreate, CartItemRead
from app.services import cart_service
from app.utils.exceptions import NotFoundError, OutOfStockError

router = APIRouter(prefix="/carts", tags=["Cart"])


@router.post("/{user_id}/items", response_model=CartItemRead, status_code=status.HTTP_201_CREATED)
def add_to_cart(user_id: int, payload: CartItemCreate, db: Session = Depends(get_db)):
    try:
        return cart_service.add_to_cart(db, user_id, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except OutOfStockError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}/items", response_model=list[CartItemRead])
def list_cart(user_id: int, db: Session = Depends(get_db)):
    return cart_service.list_cart(db, user_id)


@router.delete("/items/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db)):
    try:
        cart_service.remove_from_cart(db, cart_item_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))