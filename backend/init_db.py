#!/usr/bin/env python3
"""Initialize the ATL Pubnix database with tables and test data."""

import os
from datetime import datetime, timezone

from database import create_db_and_tables, get_db_session
from models.user import Application, ApplicationStatus, ResourceLimits, User, UserStatus


def create_test_data():
    """Create test data for development."""
    session = get_db_session()

    try:
        # Create test users
        test_users = [
            User(
                username="testuser1",
                email="testuser1@example.com",
                full_name="Test User One",
                status=UserStatus.APPROVED,
                approval_date=datetime.now(timezone.utc),
                home_directory="/home/testuser1",
                created_by="admin",
            ),
            User(
                username="testuser2",
                email="testuser2@example.com",
                full_name="Test User Two",
                status=UserStatus.APPROVED,
                approval_date=datetime.now(timezone.utc),
                home_directory="/home/testuser2",
                created_by="admin",
            ),
        ]

        for user in test_users:
            session.add(user)

        session.commit()

        # Create resource limits for test users
        for user in test_users:
            session.refresh(user)
            limits = ResourceLimits(
                user_id=user.id,
                disk_quota_mb=1024,
                max_processes=50,
                cpu_limit_percent=10,
                memory_limit_mb=512,
                max_login_sessions=5,
            )
            session.add(limits)

        # Create test application
        test_app = Application(
            email="newuser@example.com",
            username_requested="newuser",
            full_name="New User",
            motivation="I want to learn Unix and contribute to the community",
            community_guidelines_accepted=True,
            status=ApplicationStatus.PENDING,
        )
        session.add(test_app)

        session.commit()
        print("✓ Test data created successfully")

    except Exception as e:
        session.rollback()
        print(f"✗ Error creating test data: {e}")
    finally:
        session.close()


def main():
    """Initialize database and create test data."""
    print("Initializing ATL Pubnix database...")

    # Create tables
    try:
        create_db_and_tables()
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return

    # Create test data if in development mode
    if os.getenv("PUBNIX_ENV", "development") == "development":
        create_test_data()

    print("Database initialization complete!")


if __name__ == "__main__":
    main()
