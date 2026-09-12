"""API smoke tests using FastAPI's TestClient."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_login_then_me() -> None:
    login = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = client.get(
        "/api/v1/auth/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert me.status_code == 200
    assert me.json()["username"] == "admin"


def test_login_rejects_bad_credentials() -> None:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "wrong"},
    )
    assert response.status_code == 401


def test_workflow_crud_roundtrip() -> None:
    created = client.post(
        "/api/v1/workflows",
        json={
            "name": "Invoice processing",
            "trigger": "manual",
            "steps": [{"id": "s1", "action": "extract_fields", "params": {}}],
        },
    )
    assert created.status_code == 201
    workflow_id = created.json()["id"]

    listed = client.get("/api/v1/workflows")
    assert workflow_id in [w["id"] for w in listed.json()]

    run = client.post(f"/api/v1/workflows/{workflow_id}/run")
    assert run.status_code == 200
    assert run.json()["status"] == "queued"


def test_run_missing_workflow_returns_404() -> None:
    import uuid

    response = client.post(f"/api/v1/workflows/{uuid.uuid4()}/run")
    assert response.status_code == 404
