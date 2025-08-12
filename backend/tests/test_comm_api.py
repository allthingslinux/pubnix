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
def override_dependencies(session):
    def _get_session_override() -> Generator[Session, None, None]:
        yield session

    main.app.dependency_overrides[prod_get_session] = _get_session_override
    yield
    main.app.dependency_overrides.clear()


def test_send_and_list_inbox(session):
    client = TestClient(main.app)

    # Send wall message
    resp = client.post(
        "/api/v1/comm/send", json={"from_user": "alice", "content": "Hello all!"}
    )
    assert resp.status_code == 201

    # Send direct message
    resp = client.post(
        "/api/v1/comm/send",
        json={"from_user": "alice", "to_user": "bob", "content": "Hi Bob"},
    )
    assert resp.status_code == 201

    # Inbox for bob should include wall + direct
    resp = client.get("/api/v1/comm/inbox?username=bob")
    assert resp.status_code == 200
    msgs = resp.json()
    assert any(m["content"] == "Hello all!" for m in msgs)
    assert any(m["content"] == "Hi Bob" for m in msgs)


def test_send_and_list_room(session):
    client = TestClient(main.app)

    # Send room messages
    for i in range(3):
        resp = client.post(
            "/api/v1/comm/send",
            json={"from_user": "alice", "room": "general", "content": f"post {i}"},
        )
        assert resp.status_code == 201

    # Fetch room
    resp = client.get("/api/v1/comm/room/general")
    assert resp.status_code == 200
    msgs = resp.json()
    assert len(msgs) == 3
