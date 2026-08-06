# filename: app/routers/product_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product_schema import (
    CategoryCreate,
    CategoryRead,
    CategoryWithProductsRead,
    ProductCreate,
    ProductRead,
)
from app.services import product_service
from app.utils.exceptions import NotFoundError

router = APIRouter(prefix="/products", tags=["Products"])


# ---------- Category ----------
@router.post("/categories", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    return product_service.create_category(db, payload)


@router.get("/categories/{category_id}", response_model=CategoryWithProductsRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    try:
        return product_service.get_category(db, category_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ---------- Product ----------
@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    try:
        return product_service.create_product(db, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        return product_service.get_product(db, product_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    return product_service.list_products(db)
