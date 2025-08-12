"""User account and application data models for ATL Pubnix."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class UserStatus(str, Enum):
    """User account status enumeration."""

    PENDING = "pending"
    APPROVED = "approved"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class ApplicationStatus(str, Enum):
    """Application review status enumeration."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ResourceLimits(SQLModel, table=True):
    """Resource limits for user accounts."""

    __tablename__ = "resource_limits"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    disk_quota_mb: int = Field(default=1024, description="Disk quota in MB")
    max_processes: int = Field(default=50, description="Maximum concurrent processes")
    cpu_limit_percent: int = Field(default=10, description="CPU usage limit percentage")
    memory_limit_mb: int = Field(default=512, description="Memory limit in MB")
    max_login_sessions: int = Field(
        default=5, description="Maximum concurrent SSH sessions"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship back to user
    user: "User" = Relationship(back_populates="resource_limits")


class User(SQLModel, table=True):
    """User account model."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(
        min_length=3,
        max_length=32,
        regex=r"^[a-zA-Z0-9_]+$",
        unique=True,
        index=True,
        description="Unique username (3-32 chars, alphanumeric + underscore)",
    )
    email: str = Field(unique=True, index=True, description="User email address")
    full_name: str = Field(description="User's full name")
    application_date: datetime = Field(default_factory=datetime.utcnow)
    approval_date: Optional[datetime] = Field(default=None)
    status: UserStatus = Field(default=UserStatus.PENDING)
    home_directory: Optional[str] = Field(
        default=None, description="Path to user home directory"
    )
    shell: str = Field(default="/bin/bash", description="User's default shell")
    last_login: Optional[datetime] = Field(default=None)
    created_by: Optional[str] = Field(
        default=None, description="Admin who created the account"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    resource_limits: Optional[ResourceLimits] = Relationship(back_populates="user")

    def __str__(self) -> str:
        return f"User(username={self.username}, status={self.status})"


class Application(SQLModel, table=True):
    """User application model for account requests."""

    __tablename__ = "applications"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, description="Applicant email address")
    username_requested: str = Field(
        min_length=3,
        max_length=32,
        regex=r"^[a-zA-Z0-9_]+$",
        description="Requested username",
    )
    full_name: str = Field(description="Applicant's full name")
    motivation: Optional[str] = Field(
        default=None, description="Why they want an account"
    )
    community_guidelines_accepted: bool = Field(default=False)
    application_date: datetime = Field(default_factory=datetime.utcnow)
    status: ApplicationStatus = Field(default=ApplicationStatus.PENDING)
    reviewed_by: Optional[str] = Field(default=None, description="Admin who reviewed")
    review_date: Optional[datetime] = Field(default=None)
    review_notes: Optional[str] = Field(default=None, description="Admin review notes")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __str__(self) -> str:
        return f"Application(email={self.email}, username={self.username_requested}, status={self.status})"
