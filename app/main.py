from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.routers import user_router

# create tables (case-study level; use Alembic in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Shopping API")

app.include_router(user_router.router)


@app.get("/")
def root():
    return {"message": "Online Shopping API is running "}