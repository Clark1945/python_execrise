
import pytest_asyncio
import pytest
from fastapi.testclient import TestClient

# 確保 Python 能找到 fastapi_demo 模組
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi_demo.main import app
from fastapi_demo.postgre import get_db

# 建立 TestClient
client = TestClient(app)

# --- Messages 測試案例 ---

@pytest.mark.asyncio
async def test_get_messages_html():
    """
    測試 GET /messages/ 是否成功返回 WebSocket 測試頁面。
    """
    response = client.get("/messages/")
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text

def test_websocket_echo():
    """
    測試 WebSocket /ws 端點的 echo 功能。
    """
    with client.websocket_connect("/messages/ws") as websocket:
        # 1. 測試連線成功後收到的第一則訊息
        initial_message = websocket.receive_text()
        assert initial_message == "Connected to FastAPI WebSocket 🚀"

        # 2. 測試發送訊息並收到 echo
        test_message = "Hello, WebSocket!"
        websocket.send_text(test_message)
        response_message = websocket.receive_text()
        assert response_message == f"Echo: {test_message}"

        # 3. 測試發送另一則訊息
        another_test_message = "Testing again!"
        websocket.send_text(another_test_message)
        response_message = websocket.receive_text()
        assert response_message == f"Echo: {another_test_message}"
