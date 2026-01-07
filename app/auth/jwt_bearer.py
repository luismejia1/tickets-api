from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from fastapi import Depends, status
from .jwt_handler import decode_token
from app.models.token import TokenData, Token, TokenPayload
from datetime import datetime
from fastapi import HTTPException
from jose import jwt, JWTError
from pydantic import ValidationError
from typing import Optional, List

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_version}/auth/login"
)


def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        payload = decode_token(token)
        token_data = TokenPayload(**payload)

        exp = token_data.exp
        if exp is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired',
                headers={"WWW-Authenticate": "Bearer"},
            )
        if datetime.fromtimestamp(float(exp)) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired',
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data.sub

    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_with_roles(required_roles: Optional[List[str]]):
    """
    Check if current user has required role
    """

    if required_roles is None:
        required_roles = []

    def _inner(token: str = Depends(oauth2_scheme)) -> str | None:
        try:
            payload = decode_token(token)
            token_data = TokenPayload(**payload)

            exp = token_data.exp
            if exp is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired',
                    headers={"WWW-Authenticate": "Bearer"},
                )
            if datetime.fromtimestamp(float(exp)) < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired',
                    headers={"WWW-Authenticate": "Bearer"},
                )
            if not required_roles:
                return token_data.sub

            user_role = set(token_data.role)

            if user_role not in required_roles:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Insufficient permission',
                    headers={"WWW-Authenticate": "Bearer"}
                )

            return token_data.sub

        except (JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
