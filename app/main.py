from fastapi import Depends, FastAPI
from .routers import users


app = FastAPI()
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
