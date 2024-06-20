from fastapi import FastAPI

from service.attraction import router as attraction_router
from service.mrt import router as mrts_router

app = FastAPI()

app.include_router(attraction_router, tags=["Attraction"])
app.include_router(mrts_router, tags=["MRT Station"])