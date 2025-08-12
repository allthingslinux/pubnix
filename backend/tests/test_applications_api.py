from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import main
from database import get_session as prod_get_session
from models import ApplicationStatus, User, UserStatus
from routers import applications as applications_router


@pytest.fixture
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine) -> Generator[Session, None, None]:
    with Session(engine) as s:
        yield s


@pytest.fixture(autouse=True)
def override_dependencies(monkeypatch, session):
    # Override DB session dependency
    def _get_session_override() -> Generator[Session, None, None]:
        yield session

    main.app.dependency_overrides[prod_get_session] = _get_session_override

    # Disable startup DB init
    monkeypatch.setattr(main, "create_db_and_tables", lambda: None)

    # Stub admin identity
    main.app.dependency_overrides[applications_router.get_current_admin_username] = (
        lambda: "admin"
    )

    # Stub email sending to no-op
    async def _send_ok(*args, **kwargs):
        return True

    from services.email_service import EmailService

    monkeypatch.setattr(EmailService, "send_application_confirmation", _send_ok)
    monkeypatch.setattr(EmailService, "send_application_status_update", _send_ok)

    yield

    main.app.dependency_overrides.clear()


def test_submit_application_and_retrieve(session):
    client = TestClient(main.app)

    payload = {
        "email": "applicant@example.com",
        "username_requested": "new_user",
        "full_name": "New User",
        "motivation": "I want to learn Unix",
        "community_guidelines_accepted": True,
    }
    resp = client.post("/api/v1/applications/", json=payload)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["email"] == payload["email"]
    assert data["username_requested"] == payload["username_requested"]
    assert data["status"] == ApplicationStatus.PENDING

    app_id = data["id"]

    # Get by id
    resp2 = client.get(f"/api/v1/applications/{app_id}")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["id"] == app_id

    # List
    resp3 = client.get("/api/v1/applications/?limit=10")
    assert resp3.status_code == 200
    items = resp3.json()
    assert any(item["id"] == app_id for item in items)


def test_review_approve_creates_user(session):
    client = TestClient(main.app)

    # Create application
    payload = {
        "email": "user2@example.com",
        "username_requested": "approved_user",
        "full_name": "Approved User",
        "community_guidelines_accepted": True,
    }
    created = client.post("/api/v1/applications/", json=payload).json()

    # Approve
    review_payload = {
        "status": ApplicationStatus.APPROVED,
        "review_notes": "Looks good",
    }
    resp = client.patch(
        f"/api/v1/applications/{created['id']}/review", json=review_payload
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["status"] == ApplicationStatus.APPROVED

    # Verify user created
    from sqlmodel import select

    user = session.exec(
        select(User).where(User.username == payload["username_requested"])
    ).first()

    assert user is not None
    assert user.email == payload["email"]
    assert user.status == UserStatus.APPROVED
