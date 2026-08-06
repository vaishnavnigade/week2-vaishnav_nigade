from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import user_repository
from app.schemas.user_schema import UserCreate
from app.utils.exceptions import AlreadyExistsError, NotFoundError


def create_user(db: Session, data: UserCreate) -> User:
    # business rule: email must be unique
    if user_repository.get_user_by_email(db, data.email):
        raise AlreadyExistsError("Email already registered")

    user = User(
        username=data.username,
        email=data.email,
        password=data.password,  # NOTE: hash before storing in production
    )
    return user_repository.create_user(db, user)


def get_user(db: Session, user_id: int) -> User:
    user = user_repository.get_user(db, user_id)
    if user is None:
        raise NotFoundError("User not found")
    return user


def list_users(db: Session) -> list[User]:
    return user_repository.list_users(db)