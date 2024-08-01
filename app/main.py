from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import asyncio

from app.service.attraction import router as attraction_router
from app.service.mrt import router as mrts_router
from app.service.post import router as post_router
from app.service.notification import router as notification_router
from app.service.default import router as default_router
from app.manager.config import ConfigManager
from app.manager.logger import LoggerManager
from app.manager.db import DBManager
from app.manager.cache import RedisManager
from app.manager.scheduler import SchedulerManager
from app.manager.s3 import s3Manager
from app.manager.logger import LoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):

    # 初始化邏輯
    ConfigManager.init_config()
    LoggerManager.init_logger()
    DBManager.init_db()
    await RedisManager.init_redis()
    SchedulerManager.init_scheduler()
    s3Manager.init_s3()
   
    yield

    # 清理邏輯
    ConfigManager.close_config()
    LoggerManager.close_logger()
    DBManager.close_db()
    await RedisManager.close_redis()
    SchedulerManager.close_scheduler()
    s3Manager.close_s3()

class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, timeout=15):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request: Request, call_next):
        try:
            return await asyncio.wait_for(call_next(request), timeout=self.timeout)
        except asyncio.TimeoutError:
            return JSONResponse(status_code=408, content={"message": "Request timed out"})
        
app = FastAPI(lifespan=lifespan)
app.add_middleware(TimeoutMiddleware, timeout=15.0)
app.add_middleware(LoggingMiddleware)
app.include_router(attraction_router, tags=["Attraction"])
app.include_router(mrts_router, tags=["MRT Station"])
app.include_router(post_router, tags=["Post"])
app.include_router(notification_router, tags=["Notification"])
app.include_router(default_router, tags=["Default"])
