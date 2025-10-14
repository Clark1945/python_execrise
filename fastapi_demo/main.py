from fastapi import FastAPI
from . import models
from .postgre import engine
from .routers import users

# 初始化資料庫表格
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 加入 user的router
app.include_router(users.router)