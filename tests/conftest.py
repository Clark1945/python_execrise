import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
import uuid
from unittest.mock import patch

# 從你的專案中匯入 FastAPI app 和 models
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi_demo.main import app
from fastapi_demo.postgre import get_db, Base, pwd_context
from fastapi_demo import models
from fastapi_demo.minio import s3_client # 匯入真實的 s3_client 以便模擬

# --- 測試資料庫設定 ---
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
AsyncTestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# --- 依賴覆寫 (Dependency Override) ---
async def override_get_db():
    async with AsyncTestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# 建立 TestClient
client = TestClient(app)

# --- Fixtures ---

@pytest_asyncio.fixture(scope="module")
async def test_user_and_token():
    async with AsyncTestingSessionLocal() as db:
        test_username = "testuser"
        test_password = "Password123!"
        
        existing_user = await db.execute(models.User.__table__.delete().where(models.User.username == test_username))
        await db.commit()

        user = models.User(
            name="Test Fixture User",
            age=25,
            username=test_username,
            password=pwd_context.hash(test_password)
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        user_qry_id = user.qry_id

    response = client.post(
        "/tokens/",
        data={"username": test_username, "password": test_password}
    )
    assert response.status_code == 200, f"Failed to get token: {response.text}"
    token_data = response.json()
    access_token = token_data["access_token"]
    
    yield access_token, user_qry_id

