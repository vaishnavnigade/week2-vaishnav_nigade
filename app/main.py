# FastAPI is the web framework used to build and run the API.
from fastapi import FastAPI

# Base holds the shared SQLAlchemy metadata (all ORM models register against it).
from app.db.base import Base
# engine is the configured database connection used to talk to Postgres.
from app.db.sessions import engine
# Import the route handlers for each resource area of the application.
from app.routers import user_router, cart_router, order_router, product_router

# load_dotenv reads key/value pairs from the .env file into environment variables.
from dotenv import load_dotenv
# override=True makes .env values take precedence over any existing env vars.
load_dotenv(override=True)


# Create all database tables defined on the models if they don't already exist.
# Suitable for the prototype; use migrations for schema changes.
Base.metadata.create_all(bind=engine)


# Instantiate the FastAPI application with metadata shown in the auto-generated docs.
app = FastAPI(
    title="Online Shopping API",
    version="1.0.0",
    description="Backend API for the Online Shopping Application",
)


# Register each router so its endpoints become part of the application.
app.include_router(user_router.router )      # User-related endpoints
app.include_router(cart_router.router )      # Shopping cart endpoints
app.include_router(product_router.router )   # Product catalog endpoints
app.include_router(order_router.router )     # Order management endpoints


# Health-check endpoint: a simple GET on "/" to confirm the API is up.
@app.get("/", tags=["Health"])
def root() -> dict[str, str]:
    # Return a basic JSON status message.
    return {"message": "Online Shopping API is running"}