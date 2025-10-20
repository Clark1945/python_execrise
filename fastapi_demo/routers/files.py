import io
import logging

from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException, UploadFile
from starlette.responses import StreamingResponse

from ..config import settings
from ..minio import s3_client

router = APIRouter(prefix="/files", tags=["Files"])


# 上傳檔案
@router.post("/upload")
async def upload_file(file: UploadFile):
    try:
        s3_client.upload_fileobj(file.file, settings.BUCKET_NAME, file.filename)
        return {"file_name": file.filename, "bucket": settings.BUCKET_NAME}
    except ClientError as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Failed to upload file to S3")


# ---------------------------
# 下載檔案
@router.get("/download/{file_name}")
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
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise HTTPException(status_code=404, detail=f"File '{file_name}' not found in bucket '{settings.BUCKET_NAME}'")
        else:
            # For other S3 errors (permissions, etc.), log the error and return a 500
            logging.error(f"An unexpected S3 error occurred: {e}")
            raise HTTPException(status_code=500, detail="An internal error occurred while trying to download the file.")
