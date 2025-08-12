"""SSH public key model for users."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class SshKey(SQLModel, table=True):
    __tablename__ = "ssh_keys"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(min_length=1, max_length=100, description="Key label")
    public_key: str = Field(description="OpenSSH public key")
    fingerprint: str = Field(index=True, description="SHA256 fingerprint")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used_at: Optional[datetime] = Field(default=None)

    # Note: relationship to User intentionally omitted to avoid circular
    # import issues in tests; use user_id foreign key for joins when needed.
