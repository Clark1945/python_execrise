
import pytest_asyncio
import pytest
from fastapi.testclient import TestClient
import uuid

# 從你的專案中匯入 FastAPI app 和 models
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi_demo.main import app
from fastapi_demo.postgre import get_db

# 建立 TestClient
client = TestClient(app)

# --- 測試案例 ---

@pytest.mark.asyncio
async def test_list_users(test_user_and_token):
    """
    測試在有身份驗證的情況下列出所有使用者。
    """
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # 列表裡應該至少有我們 fixture 建立的使用者
    assert len(data) >= 1
    assert any(u["username"] == "testuser" for u in data)

@pytest.mark.asyncio
async def test_create_and_get_user(test_user_and_token):
    """
    測試在有身份驗證的情況下，建立一個新使用者，然後查詢該使用者。
    """
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    # 1. 建立一個新使用者
    new_username = f"new_user_{uuid.uuid4().hex}"
    response = client.post(
        "/users/",
        headers=headers,
        json={"name": "New Test User", "age": 30, "username": new_username, "password": "NewPassword123!"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "qry_id" in data
    new_user_qry_id = data["qry_id"]

    # 2. 使用 qry_id 查詢剛剛建立的使用者
    response = client.get(f"/users/{new_user_qry_id}", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "New Test User"
    assert data["username"] == new_username
    assert data["qry_id"] == str(new_user_qry_id)

@pytest.mark.asyncio
async def test_get_user_by_id(test_user_and_token):
    """
    測試使用 ID 查詢特定使用者。
    """
    access_token, user_qry_id = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get(f"/users/{user_qry_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["qry_id"] == str(user_qry_id)

@pytest.mark.asyncio
async def test_get_nonexistent_user(test_user_and_token):
    """
    測試查詢一個不存在的使用者，應返回 404 Not Found。
    """
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    nonexistent_uuid = str(uuid.uuid4())
    response = client.get(f"/users/{nonexistent_uuid}", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


@pytest.mark.asyncio
async def test_list_users(test_user_and_token):
    """
    測試在有身份驗證的情況下列出所有使用者。
    """
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # 列表裡應該至少有我們 fixture 建立的使用者
    assert len(data) >= 1
    assert any(u["username"] == "testuser" for u in data)

@pytest.mark.asyncio
async def test_create_and_get_user(test_user_and_token):
    """
    測試在有身份驗證的情況下，建立一個新使用者，然後查詢該使用者。
    """
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    # 1. 建立一個新使用者
    new_username = f"new_user_{uuid.uuid4().hex}"
    response = client.post(
        "/users/",
        headers=headers,
        json={"name": "New Test User", "age": 30, "username": new_username, "password": "NewPassword123!"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "qry_id" in data
    new_user_qry_id = data["qry_id"]

    # 2. 使用 qry_id 查詢剛剛建立的使用者
    response = client.get(f"/users/{new_user_qry_id}", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "New Test User"
    assert data["username"] == new_username
    assert data["qry_id"] == str(new_user_qry_id)

@pytest.mark.asyncio
async def test_get_user_by_id(test_user_and_token):
    """
    測試使用 ID 查詢特定使用者。
    """
    access_token, user_qry_id = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get(f"/users/{user_qry_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["qry_id"] == str(user_qry_id)

@pytest.mark.asyncio
async def test_get_nonexistent_user(test_user_and_token):
    """
    測試查詢一個不存在的使用者，應返回 404 Not Found。
    """
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    nonexistent_uuid = str(uuid.uuid4())
    response = client.get(f"/users/{nonexistent_uuid}", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
