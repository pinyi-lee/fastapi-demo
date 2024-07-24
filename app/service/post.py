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

@router.get("/", response_class=HTMLResponse)
def get_upload_page():
    return """
    <html>
        <head>
            <title>Upload to S3</title>
        </head>
        <body>
            <h1>Upload Image to S3</h1>
            <form id="upload-form">
                <input type="file" id="file-input" name="file" accept="image/*">
                <button type="button" onclick="uploadFile()">Upload</button>
            </form>
            <script>
                async function uploadFile() {
                    const fileInput = document.getElementById('file-input');
                    const file = fileInput.files[0];
                    if (!file) {
                        alert('Please select a file');
                        return;
                    }

                    const response = await fetch('/api/post/presigned_url', {
                        method: 'POST',
                    });
                    const data = await response.json();
                    const presignedUrl = data.url;

                    const xhr = new XMLHttpRequest();
                    xhr.open('PUT', presignedUrl, true);
                    xhr.setRequestHeader('Content-Type', file.type);

                    xhr.upload.onprogress = function(e) {
                        if (e.lengthComputable) {
                            const percentComplete = (e.loaded / e.total) * 100;
                            console.log(percentComplete + '% uploaded');
                        }
                    };

                    xhr.onload = function() {
                        if (xhr.status == 200) {
                            alert('File uploaded successfully');
                        } else {
                            alert('File upload failed');
                        }
                    };

                    xhr.onerror = function() {
                        alert('File upload failed');
                    };

                    xhr.send(file);
                }
            </script>
        </body>
    </html>
    """
