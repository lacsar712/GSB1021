from tests.conftest import post_login


def test_login_success():
    response = post_login("admin", "123456")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert data["message"] == "登录成功"
    assert data["data"]["username"] == "admin"
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"


def test_login_wrong_password():
    response = post_login("admin", "wrongpassword")
    assert response.status_code == 401
    data = response.json()
    assert data["code"] == 401
    assert data["message"] == "用户名或密码错误"
    assert data["data"] is None
