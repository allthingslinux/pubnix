from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import main
from database import get_session as prod_get_session


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
    def _get_session_override() -> Generator[Session, None, None]:
        yield session

    main.app.dependency_overrides[prod_get_session] = _get_session_override
    monkeypatch.setenv("INTEGRATIONS_API_KEY", "test-key")
    yield
    main.app.dependency_overrides.clear()


def test_import_export_users(session):
    client = TestClient(main.app)

    headers = {"X-API-Key": "test-key"}

    # Import
    payload = [
        {"username": "ext1", "email": "e1@example.com", "full_name": "Ext One"},
        {"username": "ext2", "email": "e2@example.com", "full_name": "Ext Two"},
    ]
    resp = client.post(
        "/api/v1/integrations/users/import", json=payload, headers=headers
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["created"] == 2

    # Export
    resp = client.get("/api/v1/integrations/users/export", headers=headers)
    assert resp.status_code == 200
    users = resp.json()
    assert {u["username"] for u in users} >= {"ext1", "ext2"}
