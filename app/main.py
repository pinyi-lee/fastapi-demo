from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.service.attraction import router as attraction_router
from app.service.mrt import router as mrts_router
from app.util.config import ConfigManager
from app.util.logger import LoggerManager
from app.database.db import DBManager
from app.service.cache import RedisManager
from app.service.scheduler import SchedulerManager
from app.util.logger import LoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 初始化邏輯
    ConfigManager.init_config()
    LoggerManager.init_logger()
    DBManager.init_db()
    RedisManager.init_redis()
    SchedulerManager.init_scheduler()
   
    yield

    # 清理邏輯
    ConfigManager.close_config()
    LoggerManager.close_logger()
    DBManager.close_db()
    RedisManager.close_redis()
    SchedulerManager.close_scheduler()

app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.include_router(attraction_router, tags=["Attraction"])
app.include_router(mrts_router, tags=["MRT Station"])