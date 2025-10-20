import uuid
from datetime import datetime, UTC
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..auth import get_current_user
from ..models import User
from ..postgre import get_db, pwd_context

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, age=user.age, username=user.username,
                          password=pwd_context.hash(user.password))
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=503, detail=str(e))
    else:
        return db_user


@router.get("/", response_model=list[schemas.UserQueryResponse])
def list_users(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get("/{user_id}", response_model=schemas.UserQueryResponse)
def get_user(user_id: uuid.UUID, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = query_user_by_id(user_id, db)

    return user


@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: uuid.UUID, updated_user: schemas.UserUpdate, current_user: str = Depends(get_current_user),
                db: Session = Depends(get_db)):
    user = query_user_by_id(user_id, db)

    user.name = updated_user.name
    user.age = updated_user.age
    user.update_time = datetime.now(UTC)
    try:
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=503, detail=str(e))
    else:
        return user


@router.delete("/{user_id}")
def delete_user(user_id: uuid.UUID, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = query_user_by_id(user_id, db)

    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=503, detail=str(e))
    else:
        return {"message": "User deleted"}

def query_user_by_id(user_id: uuid.UUID, db: Session) -> type[User]:
    user = db.query(models.User).filter(models.User.qry_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user