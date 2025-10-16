import http

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import models
from .auth import create_access_token
from .postgre import engine, verify_password, get_db
from .routers import users

# 初始化資料庫表格
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 加入 user的router
app.include_router(users.router)

@app.post("/token")
def login(db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}