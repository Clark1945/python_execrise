import re
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.v1 import validator


class UserBase(BaseModel):
    pass

# Router請求驗證格式
class UserCreate(UserBase):
    name: str
    age: int
    username: str
    password: str
    # 驗證 age
    @validator('age')
    def validate_age(self, v):
        if v < 0 or v > 100:
            raise ValueError('年齡必須在 0-100 之間')
        return v

    # 驗證 password
    @validator('password')
    def validate_password(self, v):
        if len(v) < 8:
            raise ValueError('密碼至少需要 8 個字元')

        # 檢查是否包含大寫字母
        if not re.search(r'[A-Z]', v):
            raise ValueError('密碼必須包含至少一個大寫字母')

        # 檢查是否包含小寫字母
        if not re.search(r'[a-z]', v):
            raise ValueError('密碼必須包含至少一個小寫字母')

        # 檢查是否包含數字
        if not re.search(r'\d', v):
            raise ValueError('密碼必須包含至少一個數字')

        # 檢查是否包含特殊符號
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('密碼必須包含至少一個特殊符號 (!@#$%^&*等)')

        return v

class UserUpdate(UserBase):
    name: str
    age: int

class UserQueryResponse(UserBase):
    qry_id: UUID
    name: str
    age: int
    username: str

class UserResponse(UserBase):
    qry_id: UUID
    class Config:
        orm_mode = True
