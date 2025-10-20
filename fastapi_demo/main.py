from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry

from . import models
from .middleware.api_logger import APILoggingMiddleware
from .models import Query, Mutation
from .postgre import engine
from .routers import users, tokens, files, logs, transactions, messages

# 初始化資料庫表格
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 加入 api_call_log的middleware
app.add_middleware(APILoggingMiddleware)

# 加入 user的router
app.include_router(users.router)
app.include_router(tokens.router)
app.include_router(files.router)
app.include_router(logs.router)
app.include_router(transactions.router)
app.include_router(messages.router)

# 建立 schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
# 建立 GraphQL Router
graphql_app = GraphQLRouter(schema)
# 掛載 /graphql
app.include_router(graphql_app, prefix="/graphql")
