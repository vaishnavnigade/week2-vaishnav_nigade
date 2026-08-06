from fastapi import FastAPI

from app.db.base import Base
from app.db.sessions import engine
from app.routers import user_router, cart_router, order_router, product_router

from dotenv import load_dotenv
load_dotenv(override=True)

# Suitable for the prototype; use migrations for schema changes.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Online Shopping API",
    version="1.0.0",
    description="Backend API for the Online Shopping Application",
)

app.include_router(user_router.router )
app.include_router(cart_router.router )
app.include_router(product_router.router )
app.include_router(order_router.router )

@app.get("/", tags=["Health"])
def root() -> dict[str, str]:
    return {"message": "Online Shopping API is running"}