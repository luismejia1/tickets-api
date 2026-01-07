from pydantic import BaseModel
from typing import Optional, List


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    role: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: List[str] = ["user"]
