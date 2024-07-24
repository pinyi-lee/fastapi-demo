from fastapi import FastAPI

from service.attraction import router as attraction_router
from service.mrt import router as mrts_router
from config.config import ConfigManager
from database.db import DBManager
from service.cache import RedisManager
from service.scheduler import SchedulerManager
from middlewares.logging import LoggingMiddleware

app = FastAPI()
app.add_middleware(LoggingMiddleware)
app.include_router(attraction_router, tags=["Attraction"])
app.include_router(mrts_router, tags=["MRT Station"])

@app.on_event("startup")
def startup_event():
    ConfigManager.init_config()
    DBManager.init_db()
    RedisManager.init_redis()
    SchedulerManager.init_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    ConfigManager.close_config()
    DBManager.close_db()
    RedisManager.close_redis()
    SchedulerManager.close_scheduler()