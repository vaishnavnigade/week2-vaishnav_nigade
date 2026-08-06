import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD_URL_ENCODED")
port = os.getenv("POSTGRES_PORT", "5432")
db_name = os.getenv("POSTGRES_DB")
hostname = os.getenv("POSTGRES_HOST", "localhost")

# Validate required parts (port has a default, so it's not required)
missing = [
    name
    for name, value in {
        "POSTGRES_USER": user,
        "POSTGRES_PASSWORD_URL_ENCODED": password,
        "POSTGRES_DB": db_name,
        "POSTGRES_HOST": hostname
    }.items()
    if not value
]

if missing:
    raise RuntimeError(
        f"Missing required environment variables: {', '.join(missing)}. "
        "Check your .env file."
    )

DATABASE_URL = f"postgresql://{user}:{password}@{hostname}:{port}/{db_name}"

connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Yield one database session per request and always close it."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()