import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, UUID

from .postgre import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer, default=1) # ORM 版號
    qry_id = Column(UUID(as_uuid=True),unique=True,default=uuid.uuid4, nullable=False) # 自動生成 UUID
    name = Column(String(255), index=True) # 名字
    age = Column(Integer, CheckConstraint("age>=0 AND age <= 120"))
    username = Column(String(50), unique=True, index=True) # 帳號 不可重複
    password = Column(String(500)) # 密碼 預設要存加密過後的密碼
    create_time = Column(DateTime, default=datetime.utcnow())
    update_time = Column(DateTime, default=datetime.utcnow())