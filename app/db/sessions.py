import os                              # Access environment variables.
from collections.abc import Generator # Type hint for the get_db generator function.

from dotenv import load_dotenv                       # Loads variables from a .env file.
from sqlalchemy import create_engine                 # Builds the core DB connection engine.
from sqlalchemy.orm import Session, sessionmaker     # Session type and session factory.


# Read key/value pairs from the .env file into environment variables.
load_dotenv()


# Pull individual database connection settings from the environment.
user = os.getenv("POSTGRES_USER")                          # DB username
password = os.getenv("POSTGRES_PASSWORD_URL_ENCODED")      # URL-encoded DB password (safe for URLs)
port = os.getenv("POSTGRES_PORT", "5432")                  # DB port; defaults to 5432 if not set
db_name = os.getenv("POSTGRES_DB")                         # Target database name
hostname = os.getenv("POSTGRES_HOST", "localhost")         # DB host; defaults to localhost


# Validate required parts (port has a default, so it's not required)
# Collect the names of any required variables that are missing/empty.
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


# Fail fast with a clear message if any required setting is absent.
if missing:
    raise RuntimeError(
        f"Missing required environment variables: {', '.join(missing)}. "
        "Check your .env file."
    )


# Assemble the full SQLAlchemy connection URL from the pieces above.
DATABASE_URL = f"postgresql://{user}:{password}@{hostname}:{port}/{db_name}"


# SQLite needs check_same_thread=False; other databases (like Postgres) need no special args.
connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)


# Create the engine — the central object managing DB connections/pooling.
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,   # Tests connections before use to avoid stale/dropped connections.
)


# Factory that produces new Session objects bound to the engine.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,    # Don't auto-flush pending changes before queries.
    autocommit=False,   # Require explicit commits (transaction control stays in your code).
)


# FastAPI dependency: provides a DB session for the duration of a request.
def get_db() -> Generator[Session, None, None]:
    """Yield one database session per request and always close it."""
    db = SessionLocal()   # Open a new session.

    try:
        yield db          # Hand the session to the request handler.
    finally:
        db.close()        # Always close the session, even if an error occurs.
