import http
import io

import grpc
from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse, HTMLResponse
from starlette.websockets import WebSocket
from strawberry.fastapi import GraphQLRouter
import strawberry

from . import models, transaction_pb2_grpc, transaction_pb2
from .auth import create_access_token
from .config import settings
from .middleware.api_logger import APILoggingMiddleware
from .minio import s3_client
from .models import Query, Mutation
from .mongodb import api_call_log
from .postgre import engine, verify_password, get_db
from .routers import users

# 初始化資料庫表格
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 加入 user的router
app.include_router(users.router)

# 加入 api_call_log的middleware
app.add_middleware(APILoggingMiddleware)

# 建立 schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# 建立 GraphQL Router
graphql_app = GraphQLRouter(schema)

# 掛載 /graphql
app.include_router(graphql_app, prefix="/graphql")

@app.post("/token")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# 上傳檔案
@app.post("/upload")
async def upload_file(file: UploadFile):
    try:
        s3_client.upload_fileobj(file.file, settings.BUCKET_NAME, file.filename)
        return {"file_name": file.filename, "bucket": settings.BUCKET_NAME}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# 下載檔案
@app.get("/download/{file_name}")
async def download_file(file_name: str):
    try:
        # create an in-memory binary stream
        file_obj = io.BytesIO()
        # downloads the object from S3 directly into a file-like object.
        s3_client.download_fileobj(settings.BUCKET_NAME, file_name, file_obj)

        # After downloading, the file pointer is at the end of the BytesIO stream.
        # seek(0) moves it back to the beginning, so that reading the stream starts from the start of the file.
        file_obj.seek(0)
        # StreamingResponse is a FastAPI response type that streams content to the client instead of loading it all at once.
        return StreamingResponse(file_obj, media_type="application/octet-stream",
                                 headers={"Content-Disposition": f"attachment; filename={file_name}"})
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found")


# Range-Based Pagination Api Call Log
@app.get("/logs")
def get_logs(limit: int = 10, last_id: str = None):
    query = {}
    if last_id:
        query["_id"] = {"$lt": ObjectId(last_id)}

    logs = list(api_call_log.find(query)
                .sort("_id", -1)
                .limit(limit))
    for log in logs:
        log["_id"] = str(log["_id"])
    return {
        "logs": logs,
        "next_cursor": logs[-1]["_id"] if logs else None
    }

@app.get("/transaction/{transaction_id}")
def get_transaction(transaction_id: int):
    # 建立一個到 gRPC server 的「channel」（通道）連線
    # insecure_channel 表示不使用 TLS/SSL（明文）。
    # with 區塊確保在區塊結束時自動關閉 channel（釋放資源）。
    with grpc.insecure_channel("localhost:50051") as channel:
        # 使用由 protoc 生成的 gRPC client 類別 TransactionServiceStub。
        # stub 是一個本地的 client 物件，用來呼叫遠端 gRPC 服務的方法（像 RPC 的 proxy）。
        stub = transaction_pb2_grpc.TransactionServiceStub(channel)
        response = stub.GetTransactionInfo(transaction_pb2.TransactionRequest(id=transaction_id))
        return {
            "id": response.id,
            "name": response.name,
            "email": response.email
        }


# 一個簡單的 HTML 客戶端（可直接用來測試）
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI WebSocket Demo</title>
    </head>
    <body>
        <h1>🛰️ WebSocket Echo Test</h1>
        <input id="msgInput" type="text" placeholder="Type a message...">
        <button onclick="sendMessage()">Send</button>
        <ul id="messages"></ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var li = document.createElement('li');
                li.textContent = 'Server: ' + event.data;
                messages.appendChild(li);
            };
            function sendMessage() {
                var input = document.getElementById("msgInput");
                ws.send(input.value);
                input.value = '';
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 接受連線
    await websocket.accept()
    await websocket.send_text("Connected to FastAPI WebSocket 🚀")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 Received: {data}")
            await websocket.send_text(f"Echo: {data}")
    except Exception as e:
        print("❌ Connection closed:", e)