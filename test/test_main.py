from fastapi import FastAPI
from fastapi.testclient import TestClient
from contextlib import asynccontextmanager

from app.service.attraction import router as attraction_router
from app.service.mrt import router as mrts_router
from app.manager.config import ConfigManager
from app.manager.logger import LoggerManager
from app.manager.db import DBManager
from app.manager.cache import RedisManager
from app.manager.scheduler import SchedulerManager
from app.manager.logger import LoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):    
    # 初始化邏輯
    ConfigManager.init_config()
    LoggerManager.init_logger()
    DBManager.init_db()
    await RedisManager.init_redis()
    #SchedulerManager.init_scheduler()
   
    yield

    # 清理邏輯
    ConfigManager.close_config()
    LoggerManager.close_logger()
    DBManager.close_db()
    await RedisManager.close_redis()
    #SchedulerManager.close_scheduler()

app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.include_router(attraction_router, tags=["Attraction"])
app.include_router(mrts_router, tags=["MRT Station"])

def test_mrts_200():
    with TestClient(app) as client:
        response = client.get("/api/mrts")
        assert response.status_code == 200
        assert len(response.json()["data"]) == 32

def test_attractions_200():
    with TestClient(app) as client:
        response = client.get("/api/attractions")
        assert response.status_code == 200
        assert len(response.json()["data"]) == 12

def test_attractions_200_keyword():
    with TestClient(app) as client:
        response = client.get("/api/attractions?keyword=台北")
        assert response.status_code == 200
        assert len(response.json()["data"]) == 4

def test_attractions_422():
    with TestClient(app) as client:
        response = client.get("/api/attractions?page=-1")
        assert response.status_code == 422

def test_attraction_200():
    with TestClient(app) as client:
        response = client.get("/api/attraction/1")
        assert response.status_code == 200
        assert response.json()["data"]['id'] == 1

def test_attraction_404():
    with TestClient(app) as client:
        response = client.get("/api/attraction/99")
        assert response.status_code == 404