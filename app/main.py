from fastapi import Depends, FastAPI
from .routers import users
from .settings import settings
from contextlib import asynccontextmanager
from .database.session import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/info")
async def info():
    return {
        "app_name": settings.api_name,
        "dev_email": settings.dev_email,
        "database": settings.database_url
    }
