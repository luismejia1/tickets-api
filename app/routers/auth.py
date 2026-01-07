from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.core.config import settings
from app.models.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from app.auth.utils import verify_password, get_password_hash
from datetime import timedelta
from app.auth.jwt_handler import create_access_token, create_refresh_token

fake_users = [
    {
        "first_name": "Luis",
        "last_name": "Admin",
        "email": "admin@test.com",
        "role": "admin",
        "password": "admin",   # password real
        "is_active": True,
    },
    {
        "first_name": "Ana",
        "last_name": "Agent",
        "email": "agent",
        "role": "agent",
        "password": "Agent123!",   # password real
        "is_active": True,
    },
    {
        "first_name": "Carlos",
        "last_name": "Customer",
        "email": "customer@test.com",
        "role": "customer",
        "password": "customer",  # password real
        "is_active": True,
    },
]


fake_users = [
    {**u, "hashed_password": get_password_hash(u["password"])}
    for u in fake_users
]

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post('/login', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = next(
        (u for u in fake_users if u["email"] == form_data.username), None)

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)

    access_token = create_access_token(
        subject=user["email"],
        expires_delta=access_token_expires,
        role=user["role"]
    )

    refresh_token = create_refresh_token(subject=user["email"])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
