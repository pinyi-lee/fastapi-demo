from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.service.service import bindResponse
from app.model.error import InternalServerError
from app.manager.logger import LoggerManager

router = APIRouter()
    
@router.get('/api/version',
            summary = "get version",
            description= "get version")
async def notification_sse(user_id: str):
    try:
         return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = "1.0.0"
        )
    
    except Exception as e:
        LoggerManager.error(f"get version error, error message:{e}")
        return bindResponse(InternalServerError())