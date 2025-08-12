"""Simple communication models (write/wall and bulletin messages)."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int | None = Field(default=None, primary_key=True)
    from_user: str = Field(index=True, description="Sender username")
    to_user: str | None = Field(
        default=None, index=True, description="Recipient username (None for wall)"
    )
    room: str | None = Field(
        default=None, index=True, description="Bulletin board room/channel"
    )
    content: str = Field(description="Message content")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )
