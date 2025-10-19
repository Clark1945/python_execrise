from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # .env 檔案路徑設定
    model_config = SettingsConfigDict(env_file="fastapi_demo/.env", env_file_encoding='utf-8')
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
