import uuid
from datetime import datetime, UTC
from typing import List

from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, UUID

from .postgre import Base
import strawberry


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer, default=1) # ORM 版號
    qry_id = Column(UUID(as_uuid=True),unique=True,default=uuid.uuid4, nullable=False) # 自動生成 UUID
    name = Column(String(255), index=True) # 名字
    age = Column(Integer, CheckConstraint("age>=0 AND age <= 120"))
    username = Column(String(50), unique=True, index=True) # 帳號 不可重複
    password = Column(String(500)) # 密碼 預設要存加密過後的密碼
    create_time = Column(DateTime, default=datetime.now(UTC))
    update_time = Column(DateTime, default=datetime.now(UTC))

# GraphQL Book 型別
@strawberry.type
class Book:
    id: int
    book_name: str
    author: str
    price: float
    publish_date: datetime

# 模擬資料庫
books_db: List[Book] = [
    Book(id=1, book_name="Spidarman", author="clark liu", price=100, publish_date=datetime.now(UTC)),
    Book(id=2, book_name="Batman", author="batman", price=200, publish_date=datetime.now(UTC)),
]

# Query 定義 : 用途：從伺服器獲取資料（類似 REST 的 GET）
@strawberry.type
class Query:
    @strawberry.field
    def all_books(self) -> List[Book]:
        return books_db

    @strawberry.field
    def book_by_id(self, id: int) -> Book | None:
        for book in books_db:
            if book.id == id:
                return book
        return None

# Mutation 定義 : 在伺服器端建立、更新、刪除資料（類似 REST 的 POST/PUT/DELETE）
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_book(self, name: str, email: str) -> Book:
        new_id = max([u.id for u in books_db], default=0) + 1
        new_book = Book(id=new_id, name=name, email=email)
        books_db.append(new_book)
        return new_book