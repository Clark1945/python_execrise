import os

from dotenv import load_dotenv
import boto3
from botocore.client import Config


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")


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
