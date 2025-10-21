import pytest_asyncio
import pytest
from fastapi.testclient import TestClient
import io
from botocore.exceptions import ClientError
from unittest.mock import patch # 匯入 patch

# 從你的專案中匯入 FastAPI app 和 models
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi_demo.main import app
from fastapi_demo.postgre import get_db
from fastapi_demo.config import settings # 需要 settings 來獲取 BUCKET_NAME

# 建立 TestClient
client = TestClient(app)

# --- Files 測試案例 ---

@pytest.mark.asyncio
async def test_upload_file_success(test_user_and_token):
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}
    
    file_content = b"This is a test file content."
    file_name = "test_upload.txt"
    
    with patch('fastapi_demo.routers.files.s3_client') as mock_s3_client:
        # 配置模擬對象的行為
        mock_s3_client.upload_fileobj.return_value = None # 模擬成功上傳

        response = client.post(
            "/files/upload",
            headers=headers,
            files={"file": (file_name, file_content, "text/plain")}
        )
        assert response.status_code == 200, response.text
        assert response.json() == {"file_name": file_name, "bucket": settings.BUCKET_NAME}
        mock_s3_client.upload_fileobj.assert_called_once()

@pytest.mark.asyncio
async def test_upload_file_failure(test_user_and_token):
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}
    
    file_content = b"This is a test file content."
    file_name = "test_upload_fail.txt"
    with patch('fastapi_demo.routers.files.s3_client') as mock_s3_client:
        # 配置模擬對象拋出 ClientError
        mock_s3_client.upload_fileobj.side_effect = ClientError({'Error': {'Code': 'InternalError'}}, 'upload_fileobj')

        response = client.post(
            "/files/upload",
            headers=headers,
            files={"file": (file_name, file_content, "text/plain")}
        )
        assert response.status_code == 500
        assert response.json() == {"detail": "Failed to upload file to S3"}
        mock_s3_client.upload_fileobj.assert_called_once()

@pytest.mark.asyncio
async def test_download_file_success(test_user_and_token):
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}
    
    file_content = b"Downloaded test content."
    file_name = "test_download.txt"
    
    with patch('fastapi_demo.routers.files.s3_client') as mock_s3_client:
        # 配置模擬對象的行為
        def mock_download(bucket, key, file_obj):
            file_obj.write(file_content)
        mock_s3_client.download_fileobj.side_effect = mock_download

        response = client.get(f"/files/download/{file_name}", headers=headers)
        assert response.status_code == 200
        assert response.content == file_content
        assert response.headers["content-disposition"] == f"attachment; filename={file_name}"
        mock_s3_client.download_fileobj.assert_called_once()

@pytest.mark.asyncio
async def test_download_file_not_found(test_user_and_token):
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}
    
    file_name = "non_existent_file.txt"
    with patch('fastapi_demo.routers.files.s3_client') as mock_s3_client:
        mock_s3_client.download_fileobj.side_effect = ClientError({'Error': {'Code': 'NoSuchKey'}}, 'download_fileobj')

        response = client.get(f"/files/download/{file_name}", headers=headers)
        assert response.status_code == 404
        assert response.json() == {"detail": f"File '{file_name}' not found in bucket '{settings.BUCKET_NAME}'"}
        mock_s3_client.download_fileobj.assert_called_once()

@pytest.mark.asyncio
async def test_download_file_generic_error(test_user_and_token):
    access_token, _ = test_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}
    
    file_name = "error_file.txt"
    with patch('fastapi_demo.routers.files.s3_client') as mock_s3_client:
        mock_s3_client.download_fileobj.side_effect = ClientError({'Error': {'Code': 'AccessDenied'}}, 'download_fileobj')

        response = client.get(f"/files/download/{file_name}", headers=headers)
        assert response.status_code == 500
        assert response.json() == {"detail": "An internal error occurred while trying to download the file."}
        mock_s3_client.download_fileobj.assert_called_once()
