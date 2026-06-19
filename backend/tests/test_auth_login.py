import pytest
from httpx import ASGITransport, Client

from main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    with Client(transport=transport, base_url="http://test") as c:
        yield c


def test_login_success_admin_123456(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "123456"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert data["message"] == "登录成功"
    assert data["data"]["username"] == "admin"
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"
    assert len(data["data"]["access_token"]) > 0


def test_login_failure_wrong_password(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["code"] == 401
    assert data["message"] == "用户名或密码错误"
    assert data["data"] is None
