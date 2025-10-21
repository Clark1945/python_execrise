import pytest_asyncio
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from bson import ObjectId

# 從你的專案中匯入 FastAPI app 和 models
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi_demo.main import app
from fastapi_demo.postgre import get_db

# 建立 TestClient
client = TestClient(app)

# --- Logs 測試案例 ---

@pytest.mark.asyncio
@patch('fastapi_demo.routers.logs.api_call_log') # 模擬 MongoDB collection
async def test_get_logs_no_last_id(mock_api_call_log, test_user_and_token):
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    # 模擬 MongoDB 返回的資料
    mock_logs = [
        {"_id": ObjectId("60c72b2f9b1e8c001c8e4d1a"), "method": "GET", "path": "/users", "status_code": 200},
        {"_id": ObjectId("60c72b2f9b1e8c001c8e4d1b"), "method": "POST", "path": "/items", "status_code": 201},
    ]
    
    # 模擬 find().sort().limit().to_list() 的行為
    mock_cursor = MagicMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.to_list = AsyncMock(return_value=mock_logs)
    mock_api_call_log.find.return_value = mock_cursor

    response = client.get("/logs/logs", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["logs"]) == 2
    assert data["logs"][0]["path"] == "/users"
    assert data["next_cursor"] == "60c72b2f9b1e8c001c8e4d1b"
    mock_api_call_log.find.assert_called_once_with({})

@pytest.mark.asyncio
@patch('fastapi_demo.routers.logs.api_call_log')
async def test_get_logs_with_last_id(mock_api_call_log, test_user_and_token):
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    last_id = "60c72b2f9b1e8c001c8e4d1c"
    mock_logs = [
        {"_id": ObjectId("60c72b2f9b1e8c001c8e4d1d"), "method": "PUT", "path": "/products", "status_code": 200},
    ]

    mock_cursor = MagicMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.to_list = AsyncMock(return_value=mock_logs)
    mock_api_call_log.find.return_value = mock_cursor

    response = client.get(f"/logs/logs?last_id={last_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["logs"]) == 1
    assert data["logs"][0]["path"] == "/products"
    assert data["next_cursor"] == "60c72b2f9b1e8c001c8e4d1d"
    mock_api_call_log.find.assert_called_once_with({"_id": {"$lt": ObjectId(last_id)}})

@pytest.mark.asyncio
@patch('fastapi_demo.routers.logs.api_call_log')
async def test_get_logs_empty(mock_api_call_log, test_user_and_token):
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    mock_cursor = MagicMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.to_list = AsyncMock(return_value=[]) # 模擬返回空列表
    mock_api_call_log.find.return_value = mock_cursor

    response = client.get("/logs/logs", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["logs"]) == 0
    assert data["next_cursor"] is None
    mock_api_call_log.find.assert_called_once_with({})
