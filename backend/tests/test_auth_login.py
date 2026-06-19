import asyncio

from httpx import ASGITransport, AsyncClient

from main import app


def _post_login(payload: dict):
    async def _do_request():
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            return await client.post("/api/auth/login", json=payload)

    return asyncio.run(_do_request())


def test_login_success_with_admin_account():
    response = _post_login({"username": "admin", "password": "123456"})

    assert response.status_code == 200

    body = response.json()
    assert body["code"] == 200
    assert body["message"] == "登录成功"
    assert body["data"] is not None
    assert body["data"]["username"] == "admin"
    assert body["data"]["token_type"] == "bearer"
    assert isinstance(body["data"]["access_token"], str)
    assert len(body["data"]["access_token"]) > 0


def test_login_failure_with_wrong_password():
    response = _post_login({"username": "admin", "password": "wrong-password"})

    assert response.status_code == 401

    body = response.json()
    assert body["code"] == 401
    assert body["message"] == "用户名或密码错误"
    assert body["data"] is None
