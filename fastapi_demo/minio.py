import boto3
from botocore.client import Config

from fastapi_demo.config import settings

s3_client = boto3.client(
    "s3",
    endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
    aws_access_key_id=settings.MINIO_ACCESS_KEY,
    aws_secret_access_key=settings.MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4")
)

# 確保 bucket 存在
try:
    s3_client.head_bucket(Bucket=settings.BUCKET_NAME)
except:
    s3_client.create_bucket(Bucket=settings.BUCKET_NAME)
finally:
    print("Bucket exists")
