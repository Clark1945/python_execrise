from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from fastapi_demo.utility import get_env_value

#####################################################
DATABASE_URL = get_env_value("DATABASE_URL")
#####################################################

# 建立跟資料庫溝通的核心物件
engine = create_engine(DATABASE_URL)
# 建立session工廠，用來生成Session Instance
# autocommit=False 代表需要明確呼叫 session.commit() 才會儲存，比較安全
# autoflush=False 決定 SQLAlchemy 是否在查詢前自動將記憶體中的變更「同步」到資料庫(但尚未 commit)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 密碼加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 取得 session 的 dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
