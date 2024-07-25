from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import uuid

from app.service.service import bindResponse
from app.model.error import InternalServerError
from app.service.s3 import s3Manager
from app.model.post import PresignedUrlRes
from app.util.config import ConfigManager
from app.util.logger import LoggerManager

router = APIRouter()

@router.post("/api/post/presigned_url",
            summary = "取得 post presigned url",
            description="取得 post presigned url")
def generate_presigned_url():
    try:
        response = s3Manager.get_s3().generate_presigned_url(
            'put_object',
            Params={'Bucket': ConfigManager.get_config().bucket_name, 'Key': uuid.uuid4().hex},
            ExpiresIn=3600)
    except Exception as e:
        LoggerManager.error(f"get post presigned url error, error message:{e}")
        return bindResponse(InternalServerError())
    return bindResponse(PresignedUrlRes(url = response))

@router.get("/post", response_class=HTMLResponse)
def get_upload_page():
    with open("app/static/post.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)
