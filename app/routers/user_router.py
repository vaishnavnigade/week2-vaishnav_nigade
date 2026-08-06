from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user_schema import UserLogin, UserRegister, UserResponse
from app.services import user_service
from app.utils.exceptions import AlreadyExistsError, InvalidCredentialsError

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegister, db: Session = Depends(get_db)):
    try:
        user = user_service.register_user(db, payload)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"email": user.email, "message": "User registered successfully"}


@router.post("/login", response_model=UserResponse)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    try:
        user = user_service.login_user(db, payload)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return {"email": user.email, "message": "Login successful"}