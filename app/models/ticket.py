from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Column, DateTime, Relationship
from .user import User, UserPublic
from datetime import datetime
from app.utils import get_utc_now
from sqlalchemy import func


class Status(Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    CLOSED = 'closed'


class Priority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class BaseTicket(SQLModel):
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    priority: Priority = Field(default=Priority.MEDIUM)
    status: Status = Field(default=Status.OPEN)


class Ticket(BaseTicket, table=True):
    id: int | None = Field(primary_key=True, default=None)
    assigned_to: int | None = Field(default=None, foreign_key='user.id')
    created_by: int | None = Field(default=None, foreign_key='user.id')

    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        default_factory=get_utc_now,
    )

    assigned_to_user: Optional[User] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[Ticket.assigned_to]"
        }
    )

    created_by_user: Optional[User] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[Ticket.created_by]"
        }
    )


class TicketPublic(BaseTicket, table=False):
    id: int
    created_at: datetime
    assigned_to: int
    created_by: int

    assigned_to_detail: UserPublic | None
    created_by_detail: UserPublic


class TicketCreate(Ticket, table=False):
    """I need validate all fields"""
    pass


class TicketHistory(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    ticket_id: int | None = Field(default=None, foreign_key='ticket.id')
    field_changed: str = Field(nullable=False)
    old_value: str | None = Field(nullable=True, default=None)
    change_by: int | None = Field(default=None, foreign_key='user.id')

    changed_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        default_factory=get_utc_now,
    )
