from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import asyncio

from app.service.service import bindResponse
from app.model.error import InternalServerError
from app.manager.logger import LoggerManager

router = APIRouter()
    
@router.get('/api/version',
            summary = "get version",
            description= "get version")
async def get_version():
    try:
         return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = "1.0.0"
        )
    
    except Exception as e:
        LoggerManager.error(f"get version error, error message:{e}")
        return bindResponse(InternalServerError())
    
@router.get("/api/timeout")
async def example_endpoint():
    await asyncio.sleep(10)
    return {"message": "This should timeout"}