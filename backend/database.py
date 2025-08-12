"""Database configuration and connection management for ATL Pubnix."""

import os
from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://pubnix:dev_password_change_in_production@localhost:5432/pubnix_dev",
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("PUBNIX_DEBUG", "false").lower() == "true",
    pool_pre_ping=True,
    pool_recycle=300,
)


def create_db_and_tables():
    """Create database tables from SQLModel definitions."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session for dependency injection."""
    with Session(engine) as session:
        yield session


def get_db_session() -> Session:
    """Get database session for direct use."""
    return Session(engine)
