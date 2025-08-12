"""Unit tests for ATL Pubnix data models."""

from datetime import datetime

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from models.metrics import SystemMetrics, UserMetrics
from models.user import Application, ApplicationStatus, ResourceLimits, User, UserStatus


@pytest.fixture
def session():
    """Create test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestUser:
    """Test User model validation and constraints."""

    def test_create_valid_user(self, session):
        """Test creating a valid user."""
        user = User(
            username="testuser", email="test@example.com", full_name="Test User"
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.status == UserStatus.PENDING
        assert user.shell == "/bin/bash"
        assert user.created_at is not None

    def test_username_validation(self, session):
        """Test username validation rules."""
        # Valid usernames
        valid_usernames = ["user", "test_user", "user123", "a" * 32]
        for username in valid_usernames:
            user = User(
                username=username,
                email=f"{username}@example.com",
                full_name="Test User",
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            assert user.username == username
            session.delete(user)
            session.commit()

    def test_username_uniqueness(self, session):
        """Test that usernames must be unique."""
        user1 = User(
            username="duplicate", email="user1@example.com", full_name="User One"
        )
        user2 = User(
            username="duplicate", email="user2@example.com", full_name="User Two"
        )

        session.add(user1)
        session.commit()

        session.add(user2)
        with pytest.raises(Exception):  # Should raise integrity error
            session.commit()

    def test_email_uniqueness(self, session):
        """Test that emails must be unique."""
        user1 = User(
            username="user1", email="duplicate@example.com", full_name="User One"
        )
        user2 = User(
            username="user2", email="duplicate@example.com", full_name="User Two"
        )

        session.add(user1)
        session.commit()

        session.add(user2)
        with pytest.raises(Exception):  # Should raise integrity error
            session.commit()


class TestResourceLimits:
    """Test ResourceLimits model."""

    def test_create_resource_limits(self, session):
        """Test creating resource limits."""
        user = User(
            username="testuser", email="test@example.com", full_name="Test User"
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        limits = ResourceLimits(
            user_id=user.id,
            disk_quota_mb=2048,
            max_processes=100,
            cpu_limit_percent=20,
            memory_limit_mb=1024,
            max_login_sessions=10,
        )
        session.add(limits)
        session.commit()
        session.refresh(limits)

        assert limits.id is not None
        assert limits.user_id == user.id
        assert limits.disk_quota_mb == 2048
        assert limits.max_processes == 100

    def test_default_values(self, session):
        """Test default resource limit values."""
        user = User(
            username="testuser", email="test@example.com", full_name="Test User"
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        limits = ResourceLimits(user_id=user.id)
        session.add(limits)
        session.commit()
        session.refresh(limits)

        assert limits.disk_quota_mb == 1024
        assert limits.max_processes == 50
        assert limits.cpu_limit_percent == 10
        assert limits.memory_limit_mb == 512
        assert limits.max_login_sessions == 5


class TestApplication:
    """Test Application model."""

    def test_create_application(self, session):
        """Test creating a user application."""
        app = Application(
            email="applicant@example.com",
            username_requested="newuser",
            full_name="New User",
            motivation="I want to learn Unix",
            community_guidelines_accepted=True,
        )
        session.add(app)
        session.commit()
        session.refresh(app)

        assert app.id is not None
        assert app.email == "applicant@example.com"
        assert app.username_requested == "newuser"
        assert app.status == ApplicationStatus.PENDING
        assert app.community_guidelines_accepted is True
        assert app.application_date is not None

    def test_application_review(self, session):
        """Test application review workflow."""
        app = Application(
            email="applicant@example.com",
            username_requested="newuser",
            full_name="New User",
            community_guidelines_accepted=True,
        )
        session.add(app)
        session.commit()
        session.refresh(app)

        # Approve application
        app.status = ApplicationStatus.APPROVED
        app.reviewed_by = "admin"
        app.review_date = datetime.utcnow()
        app.review_notes = "Approved - good motivation"

        session.add(app)
        session.commit()
        session.refresh(app)

        assert app.status == ApplicationStatus.APPROVED
        assert app.reviewed_by == "admin"
        assert app.review_date is not None
        assert app.review_notes == "Approved - good motivation"


class TestSystemMetrics:
    """Test SystemMetrics model."""

    def test_create_system_metrics(self, session):
        """Test creating system metrics."""
        metrics = SystemMetrics(
            total_users=100,
            active_users_24h=25,
            cpu_usage_percent=45.5,
            memory_usage_percent=60.2,
            disk_usage_percent=30.1,
            network_connections=150,
            ssh_sessions=12,
            web_requests_per_hour=500,
        )
        session.add(metrics)
        session.commit()
        session.refresh(metrics)

        assert metrics.id is not None
        assert metrics.total_users == 100
        assert metrics.active_users_24h == 25
        assert metrics.cpu_usage_percent == 45.5
        assert metrics.timestamp is not None


class TestUserMetrics:
    """Test UserMetrics model."""

    def test_create_user_metrics(self, session):
        """Test creating user metrics."""
        metrics = UserMetrics(
            username="testuser",
            cpu_time_seconds=3600,
            memory_usage_mb=256,
            disk_usage_mb=512,
            active_processes=5,
            login_sessions=2,
            last_activity=datetime.utcnow(),
            web_requests_count=50,
        )
        session.add(metrics)
        session.commit()
        session.refresh(metrics)

        assert metrics.id is not None
        assert metrics.username == "testuser"
        assert metrics.cpu_time_seconds == 3600
        assert metrics.memory_usage_mb == 256
        assert metrics.timestamp is not None
