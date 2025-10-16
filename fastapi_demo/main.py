import http
import io

from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from . import models
from .auth import create_access_token
from .midddleware.api_logger import APILoggingMiddleware
from .minio import BUCKET_NAME, s3_client
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

@app.post("/token")
def login(db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# 上傳檔案
@app.post("/upload")
async def upload_file(file: UploadFile):
    try:
        s3_client.upload_fileobj(file.file, BUCKET_NAME, file.filename)
        return {"file_name": file.filename, "bucket": BUCKET_NAME}
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
        s3_client.download_fileobj(BUCKET_NAME, file_name, file_obj)

        # After downloading, the file pointer is at the end of the BytesIO stream.
        # seek(0) moves it back to the beginning, so that reading the stream starts from the start of the file.
        file_obj.seek(0)
        # StreamingResponse is a FastAPI response type that streams content to the client instead of loading it all at once.
        return StreamingResponse(file_obj, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={file_name}"})
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