from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.sessions import get_db
from app.schemas.order_schema import OrderRead
from app.services import order_service
from app.utils.exceptions import NotFoundError, OutOfStockError

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/{user_id}/checkout", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def checkout(user_id: int, db: Session = Depends(get_db)):
    try:
        return order_service.create_order_from_cart(db, user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except OutOfStockError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        return order_service.get_order(db, order_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/users/{user_id}", response_model=list[OrderRead])
def list_orders(user_id: int, db: Session = Depends(get_db)):
    return order_service.list_orders(db, user_id)