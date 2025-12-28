from fastapi import APIRouter, Depends
from ..dependencies import get_token_header

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
    dependencies=[Depends(dependency=get_token_header)]
)


@router.get("/")
async def get_users():
    return {"message": "List of users", "data": [{"username": "Luis"}, {"username": "Alexa"}]}
