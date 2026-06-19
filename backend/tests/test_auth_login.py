import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import Base, get_db
from models import User
from routers.auth import get_password_hash

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    admin_user = User(
        username="admin",
        hashed_password=get_password_hash("123456")
    )
    db.add(admin_user)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


def test_login_success():
    async def run_test():
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:
            response = await client.post(
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
    asyncio.run(run_test())


def test_login_wrong_password():
    async def run_test():
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/auth/login",
                json={"username": "admin", "password": "wrongpass"}
            )
            assert response.status_code == 401
            data = response.json()
            assert data["code"] == 401
            assert data["message"] == "用户名或密码错误"
            assert data["data"] is None
    asyncio.run(run_test())
