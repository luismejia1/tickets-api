from sqlmodel import SQLModel, Session, Field, Enum as SAEnum, Column, DateTime
from typing import Optional
from enum import Enum
from datetime import datetime, timezone
from ..utils import get_utc_now
from sqlalchemy import func


class Role(Enum):
    ADMIN = 'admin'
    AGENT = 'agent'
    CUSTOMER = 'customer'


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    role: Role = Field(
        sa_column=SAEnum(Role, name="role_enum")
    )
    email: str = Field(default=None, unique=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        default_factory=get_utc_now,
    )
    is_active: bool = Field(default=True)
