import grpc
import pytest_asyncio
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# 從你的專案中匯入 FastAPI app 和 models
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi_demo.main import app
from fastapi_demo.postgre import get_db
from fastapi_demo import transaction_pb2 # 需要這個來建立模擬的回應物件

# 建立 TestClient
client = TestClient(app)

# --- Transactions 測試案例 ---

@pytest.mark.asyncio
@patch('fastapi_demo.routers.transactions.transaction_pb2_grpc.TransactionServiceStub') # 模擬 gRPC stub
async def test_get_transaction_success(mock_stub_class, test_user_and_token):
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    transaction_id = 123
    mock_response = transaction_pb2.TransactionResponse(id=transaction_id, name="Test Transaction", email="test@example.com")

    # 模擬 gRPC stub 的行為
    mock_stub_instance = MagicMock()
    mock_stub_instance.GetTransactionInfo.return_value = mock_response
    mock_stub_class.return_value = mock_stub_instance

    response = client.get(f"/transactions/transaction/{transaction_id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "id": mock_response.id,
        "name": mock_response.name,
        "email": mock_response.email
    }
    mock_stub_instance.GetTransactionInfo.assert_called_once_with(transaction_pb2.TransactionRequest(id=transaction_id))

@pytest.mark.asyncio
@patch('fastapi_demo.routers.transactions.transaction_pb2_grpc.TransactionServiceStub') # 模擬 gRPC stub
async def test_get_transaction_grpc_error(mock_stub_class, test_user_and_token):
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    transaction_id = 456

    # 模擬 gRPC stub 拋出異常
    mock_stub_instance = MagicMock()
    rpc_error = grpc.RpcError("gRPC error occurred")
    rpc_error.details = lambda: "gRPC error occurred"
    mock_stub_instance.GetTransactionInfo.side_effect = rpc_error
    mock_stub_class.return_value = mock_stub_instance

    response = client.get(f"/transactions/transaction/{transaction_id}", headers=headers)
    # gRPC 錯誤通常會導致 500 Internal Server Error
    assert response.status_code == 500
    assert "detail" in response.json()
    assert "gRPC error occurred" in response.json()["detail"]
    mock_stub_instance.GetTransactionInfo.assert_called_once_with(transaction_pb2.TransactionRequest(id=transaction_id))
