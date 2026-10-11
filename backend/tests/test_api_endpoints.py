import io
import pytest
from fastapi.testclient import TestClient
from main import app
from memory.session_auth import auth_manager

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"Status": "ok"}


def test_session_creation():
    response = client.post("/session")
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "session_token" in data
    assert len(data["session_id"]) >= 16
    assert len(data["session_token"]) >= 32

    # Verify session is validated by manager
    assert auth_manager.validate_session(data["session_id"], data["session_token"]) is True


def test_chat_unauthorized_without_token():
    # Attempting to use a session ID without valid token
    response = client.post(
        "/chat",
        json={"message": "hello", "session_id": "arbitrary_unauthorized_id"}
    )
    assert response.status_code == 401
    assert "Unauthorized" in response.json().get("detail", "")


def test_chat_unauthorized_with_wrong_token():
    session_res = client.post("/session").json()
    sid = session_res["session_id"]

    response = client.post(
        "/chat",
        json={
            "message": "hello",
            "session_id": sid,
            "session_token": "wrong_invalid_token_1234567890"
        }
    )
    assert response.status_code == 401


def test_upload_unauthorized_without_token():
    csv_bytes = b"category,amount\nFood,25\n"
    response = client.post(
        "/upload",
        data={"session_id": "unauth_session_id"},
        files={"file": ("expenses.csv", io.BytesIO(csv_bytes), "text/csv")}
    )
    assert response.status_code == 401


def test_upload_authorized_with_valid_token():
    session_res = client.post("/session").json()
    sid = session_res["session_id"]
    token = session_res["session_token"]

    csv_bytes = b"category,amount\nGroceries,150.0\n"
    response = client.post(
        "/upload",
        data={"session_id": sid, "session_token": token},
        files={"file": ("expenses.csv", io.BytesIO(csv_bytes), "text/csv")}
    )
    assert response.status_code == 200
    assert "Successfully uploaded" in response.json()["response"]
