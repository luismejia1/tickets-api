from enum import Enum
from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field, Column, DateTime, Relationship
from sqlalchemy import func

from .user import User, UserPublic
from app.utils import get_utc_now


class Status(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class BaseTicket(SQLModel):
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    priority: Priority = Field(default=Priority.MEDIUM)
    status: Status = Field(default=Status.OPEN)


class Ticket(BaseTicket, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    assigned_to: Optional[int] = Field(default=None, foreign_key="user.id")
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")

    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        default_factory=get_utc_now,
    )

    assigned_to_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Ticket.assigned_to]"}
    )
    created_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Ticket.created_by]"}
    )


class TicketCreate(BaseTicket):
    assigned_to: Optional[int] = None


class TicketPublic(BaseTicket):
    id: int
    created_at: datetime
    assigned_to: Optional[int]
    created_by: Optional[int]

    assigned_to_detail: Optional[UserPublic] = None
    created_by_detail: Optional[UserPublic] = None


class TicketHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    ticket_id: Optional[int] = Field(default=None, foreign_key="ticket.id")
    field_changed: str = Field(nullable=False)
    old_value: Optional[str] = Field(default=None, nullable=True)
    change_by: Optional[int] = Field(default=None, foreign_key="user.id")

    changed_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        default_factory=get_utc_now,
    )
