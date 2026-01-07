from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, List
from jose import jwt
from app.core.config import settings
from app.utils import get_utc_now


def create_access_token(subject: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    utc = get_utc_now()
    if expires_delta:
        expire = utc + expires_delta

    else:
        expire = utc + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": utc,
        "role": role
    }

    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )

    return encoded_jwt


def create_refresh_token(subject: str) -> str:
    utc = get_utc_now()
    expire = utc + timedelta(days=settings.refresh_token_expire_days)
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": utc,
        "token_type": "refresh"
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode JWT token
    """
    payload = jwt.decode(
        token, settings.secret_key, algorithms=[settings.algorithm]
    )
    return payload
