from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import main
from database import get_session as prod_get_session
from models import User


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
def override_dependencies(session):
    def _get_session_override() -> Generator[Session, None, None]:
        yield session

    main.app.dependency_overrides[prod_get_session] = _get_session_override
    yield
    main.app.dependency_overrides.clear()


def setup_user(session: Session):
    user = User(username="sshuser", email="sshuser@example.com", full_name="SSH User")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_add_list_deactivate_delete_key(session):
    client = TestClient(main.app)
    setup_user(session)

    good_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGZha2VfYmFzZTY0X2RhdGFfZm9yX3Rlc3Q= test@atl.sh"

    # Add
    resp = client.post(
        "/api/v1/ssh-keys/",
        json={"username": "sshuser", "name": "laptop", "public_key": good_key},
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["fingerprint"]

    # List
    resp = client.get("/api/v1/ssh-keys/?username=sshuser")
    assert resp.status_code == 200
    keys = resp.json()
    assert len(keys) == 1

    key_id = keys[0]["id"]

    # Deactivate
    resp = client.post(f"/api/v1/ssh-keys/{key_id}/deactivate")
    assert resp.status_code == 200
    assert resp.json()["is_active"] is False

    # Delete
    resp = client.delete(f"/api/v1/ssh-keys/{key_id}")
    assert resp.status_code == 204


def test_reject_invalid_key(session):
    client = TestClient(main.app)
    setup_user(session)

    bad_key = "ssh-ed25519 not_base64_here"
    resp = client.post(
        "/api/v1/ssh-keys/",
        json={"username": "sshuser", "name": "bad", "public_key": bad_key},
    )
    assert resp.status_code == 400
