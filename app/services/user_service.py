from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import user_repository
from app.schemas.user_schema import UserLogin, UserRegister
from app.utils.exceptions import AlreadyExistsError, InvalidCredentialsError
from app.utils.helpers import hash_password, verify_password


def register_user(db: Session, data: UserRegister) -> User:
    # same check as training: "User already exists"
    if user_repository.get_user_by_email(db, data.email):
        raise AlreadyExistsError("User already exists")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    return user_repository.create_user(db, user)


def login_user(db: Session, data: UserLogin) -> User:
    stored_user = user_repository.get_user_by_email(db, data.email)

    # same as training: fail identically for missing user OR wrong password
    if not stored_user:
        raise InvalidCredentialsError("Invalid email or password")

    if not verify_password(data.password, stored_user.hashed_password):
        raise InvalidCredentialsError("Invalid email or password")

    return stored_user