from sqlmodel import SQLModel, Session, Field, Enum as SAEnum, Column, DateTime
from typing import Optional
from enum import Enum
from datetime import datetime, timezone
from ..utils import get_utc_now
from sqlalchemy import func
from pydantic import EmailStr


class Role(Enum):
    ADMIN = 'admin'
    AGENT = 'agent'
    CUSTOMER = 'customer'


class UserBase(SQLModel):
    first_name: str
    last_name: str
    role: Role = Field(default=Role.CUSTOMER)
    email: EmailStr = Field(unique=True, index=True)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        default_factory=get_utc_now,
    )


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    role: Role | None = None
    is_active: bool | None = None
