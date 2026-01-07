from fastapi import Depends, FastAPI
from .routers import users, auth
from .core.config import settings
from contextlib import asynccontextmanager
from .database.session import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title=settings.api_name,
              openapi_url=f"{settings.api_version}/openapi.json")

app.include_router(users.router, prefix=settings.api_version)
app.include_router(auth.router, prefix=settings.api_version)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/info")
async def info():
    return {
        "app_name": settings.api_name,
        "dev_email": settings.dev_email,
    }
