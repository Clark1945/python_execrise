from fastapi_demo.utility import get_env_value
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# # Store all env properties
# SECRET_KEY = get_env_value("SECRET_KEY")
# ALGORITHM = get_env_value("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = get_env_value("ACCESS_TOKEN_EXPIRE_MINUTES")
# MINIO_ENDPOINT = get_env_value("MINIO_ENDPOINT")
# MINIO_ACCESS_KEY = get_env_value("MINIO_ACCESS_KEY")
# MINIO_SECRET_KEY = get_env_value("MINIO_SECRET_KEY")
# BUCKET_NAME = get_env_value("BUCKET_NAME")
# MONGO_URI = get_env_value("MONGO_URI")
# DB_NAME = get_env_value("DB_NAME")
# DATABASE_URL = get_env_value("DATABASE_URL")


class Settings(BaseSettings):
    # .env 檔案路徑設定
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')
     # PostgreSQL
    DATABASE_URL: str
     # MongoDB
    MONGO_URI: str
    DB_NAME: str
     # MinIO
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    BUCKET_NAME: str
    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


# 使用 lru_cache 來確保 Settings 只被實例化一次 (Singleton pattern)
@lru_cache
def get_settings():
    return Settings()
settings = get_settings()

