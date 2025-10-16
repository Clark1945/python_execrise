import boto3
from botocore.client import Config

from fastapi_demo.utility import get_env_value

#####################################################
MINIO_ENDPOINT = get_env_value("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = get_env_value("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = get_env_value("MINIO_SECRET_KEY")
BUCKET_NAME = get_env_value("BUCKET_NAME")
#####################################################

s3_client = boto3.client(
    "s3",
    endpoint_url=f"http://{MINIO_ENDPOINT}",
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4")
)

# 確保 bucket 存在
try:
    s3_client.head_bucket(Bucket=BUCKET_NAME)
except:
    s3_client.create_bucket(Bucket=BUCKET_NAME)
finally:
    print("Bucket exists")
