from fastapi import FastAPI

from service.attraction import router as attraction_router
from service.mrt import router as mrts_router
from middlewares.logging import LoggingMiddleware

app = FastAPI()
app.add_middleware(LoggingMiddleware)

app.include_router(attraction_router, tags=["Attraction"])
app.include_router(mrts_router, tags=["MRT Station"])