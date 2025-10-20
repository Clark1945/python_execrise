from contextlib import asynccontextmanager

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from fastapi_demo.config import settings
import asyncio

# 建立跟資料庫溝通的核心物件
engine = create_async_engine(settings.DATABASE_URL)
# 建立session工廠，用來生成Session Instance
# autocommit=False 代表需要明確呼叫 session.commit() 才會儲存，比較安全
# autoflush=False 決定 SQLAlchemy 是否在查詢前自動將記憶體中的變更「同步」到資料庫(但尚未 commit)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()




# 初始化密碼加密模式
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 取得 session 的 dependency
@asynccontextmanager
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
