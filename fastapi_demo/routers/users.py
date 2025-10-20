import uuid
from datetime import datetime, UTC
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from .. import models, schemas
from ..auth import get_current_user
from ..models import User
from ..postgre import get_db, pwd_context

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_user = models.User(name=user.name, age=user.age, username=user.username,
                          password=pwd_context.hash(user.password))
    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=503, detail=str(e))
    else:
        return db_user


@router.get("/", response_model=list[schemas.UserQueryResponse])
async def list_users(current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> list[User]:
    query = select(models.User)
    result = await db.execute(query)
    users = list(result.scalars().all())
    return users


@router.get("/{user_id}", response_model=schemas.UserQueryResponse)
async def get_user(user_id: uuid.UUID, current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await query_user_by_id(user_id, db)

    return user


@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user(user_id: uuid.UUID, updated_user: schemas.UserUpdate, current_user: str = Depends(get_current_user),
                db: AsyncSession = Depends(get_db)):
    user = await query_user_by_id(user_id, db)

    user.name = updated_user.name
    user.age = updated_user.age
    user.update_time = datetime.now(UTC)
    try:
        await db.commit()
        await db.refresh(user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=503, detail=str(e))
    else:
        return user


@router.delete("/{user_id}")
async def delete_user(user_id: uuid.UUID, current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await query_user_by_id(user_id, db)

    try:
        await db.delete(user)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=503, detail=str(e))
    else:
        return {"message": "User deleted"}

async def query_user_by_id(user_id: uuid.UUID, db: AsyncSession) -> User | None:
    query = select(models.User).filter(models.User.qry_id == user_id) # 建立查詢
    result = await db.execute(query) # 非同步執行
    user = result.scalars().first()  # 取出 ORM 物件
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user