
import pytest_asyncio
import pytest
from fastapi.testclient import TestClient
from fastapi import status

# 從你的專案中匯入 FastAPI app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi_demo.main import app

# 建立 TestClient
client = TestClient(app)

# --- 測試案例 ---

@pytest.mark.asyncio
async def test_login_for_access_token(test_user_and_token):
    """
    測試成功登入並取得 access token。
    這個測試主要依賴 `test_user_and_token` fixture 來執行登入流程，
    如果 fixture 成功執行（即拿到 token），就代表登入端點基本正常。
    """
    access_token, _ = test_user_and_token
    assert access_token is not None
    # 也可以在這裡加入更多對 token 格式的驗證 (例如，是否為 JWT)
    assert isinstance(access_token, str)

@pytest.mark.asyncio
async def test_login_with_invalid_credentials():
    """
    測試使用無效的憑證登入，應返回 401 Unauthorized。
    """
    response = client.post(
        "/tokens/",
        data={"username": "wronguser", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials"}

@pytest.mark.asyncio
async def test_login_with_wrong_password(test_user_and_token):
    """
    測試使用正確使用者名稱但錯誤密碼登入，應返回 401 Unauthorized。
    """
    # 我們需要從 fixture 中取得使用者名稱，但不需要 token
    # 不過 fixture 的設計是建立使用者後就直接去申請 token
    # 這裡我們就利用已建立的 "testuser" 來測試
    response = client.post(
        "/tokens/",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials"}
