from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import main
from database import get_session as prod_get_session
from models import Application, ApplicationStatus, ResourceLimits, User, UserStatus


@pytest.fixture
def engine():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine) -> Generator[Session, None, None]:
    with Session(engine) as s:
        yield s


@pytest.fixture(autouse=True)
def override_dependencies(session):
    def _get_session_override() -> Generator[Session, None, None]:
        yield session

    main.app.dependency_overrides[prod_get_session] = _get_session_override
    yield
    main.app.dependency_overrides.clear()


def seed_data(session: Session):
    u1 = User(username="u1", email="u1@example.com", full_name="U One", status=UserStatus.APPROVED)
    u2 = User(username="u2", email="u2@example.com", full_name="U Two", status=UserStatus.SUSPENDED)
    u3 = User(username="u3", email="u3@example.com", full_name="U Three", status=UserStatus.PENDING)
    session.add(u1)
    session.add(u2)
    session.add(u3)
    session.commit()
    session.refresh(u1)
    session.add(ResourceLimits(user_id=u1.id))
    session.add(Application(email="a@example.com", username_requested="new", full_name="New", status=ApplicationStatus.PENDING))
    session.commit()


def test_list_users_suspend_unsuspend_limits_and_health(session):
    seed_data(session)
    client = TestClient(main.app)

    # List users
    resp = client.get("/api/v1/admin/users")
    assert resp.status_code == 200
    users = resp.json()
    assert len(users) == 3

    # Suspend u1
    uid = users[0]["id"]
    resp = client.post(f"/api/v1/admin/users/{uid}/suspend", json={"reason": "policy"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "suspended"

    # Unsuspend
    resp = client.post(f"/api/v1/admin/users/{uid}/unsuspend")
    assert resp.status_code == 200
    assert resp.json()["status"] == "approved"

    # Update limits
    resp = client.patch(f"/api/v1/admin/users/{uid}/limits", json={"disk_quota_mb": 2048})
    assert resp.status_code == 200
    assert resp.json()["limits"]["disk_quota_mb"] == 2048

    # Health summary
    resp = client.get("/api/v1/admin/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "system" in data and "summary" in data
