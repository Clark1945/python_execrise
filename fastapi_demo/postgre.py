from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# 建立跟資料庫溝通的核心物件
engine = create_engine(DATABASE_URL)
# 建立session工廠，用來生成Session Instance
# autocommit=False 代表需要明確呼叫 session.commit() 才會儲存，比較安全
# autoflush=False 決定 SQLAlchemy 是否在查詢前自動將記憶體中的變更「同步」到資料庫(但尚未 commit)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 取得 session 的 dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
