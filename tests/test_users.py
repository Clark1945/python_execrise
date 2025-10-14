
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import uuid  # 匯入 uuid 模組

# 從你的專案中匯入 FastAPI app 和 models
# 我們需要調整路徑讓 Python 能夠找到 fastapi_demo 模組
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi_demo.main import app
from fastapi_demo.postgre import get_db, Base
from fastapi_demo import models

# --- 測試資料庫設定 ---
# 使用記憶體中的 SQLite 資料庫進行測試
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # 使用 StaticPool 讓所有連線使用同一個記憶體中資料庫實例
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 在測試開始前建立資料庫表格
Base.metadata.create_all(bind=engine)

# --- 依賴覆寫 (Dependency Override) ---
# 定義一個新的 get_db 函式，專門給測試使用
def override_get_db():
    database = None
    try:
        database = TestingSessionLocal()
        yield database
    finally:
        if database:
            database.close()

# 將應用程式中的 get_db 依賴替換為我們的測試版本
app.dependency_overrides[get_db] = override_get_db

# 建立 TestClient
client = TestClient(app)


# --- 測試案例 ---

def test_create_and_get_user():
    """
    測試建立使用者，然後查詢該使用者以驗證正確性。
    """
    # 1. 建立一個新使用者
    response = client.post(
        "/users/",
        json={"name": "Test User", "age": 30, "username": "testuser", "password": "Password123!"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    # UserResponse model 只有 qry_id，所以只檢查它
    assert "qry_id" in data
    user_qry_id = data["qry_id"]

    # 2. 使用 qry_id 查詢剛剛建立的使用者
    response = client.get(f"/users/{user_qry_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    # UserQueryResponse 包含所有欄位，現在可以完整檢查
    assert data["name"] == "Test User"
    assert data["username"] == "testuser"
    assert data["qry_id"] == user_qry_id

def test_get_nonexistent_user():
    """
    測試查詢一個不存在的使用者，應返回 404 Not Found。
    """
    # 使用一個格式正確但不存在的 UUID
    nonexistent_uuid = str(uuid.uuid4())
    response = client.get(f"/users/{nonexistent_uuid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_list_users():
    """
    測試列出所有使用者。
    """
    # 先清空一下（可選，因為每個測試函式都應該是獨立的）
    # 這裡我們知道至少有一個使用者是從上個測試建立的
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # 檢查列表裡是否至少有一個使用者
    assert len(data) > 0
    assert data[0]["username"] == "testuser"
