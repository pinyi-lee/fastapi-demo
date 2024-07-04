# test_main.py
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_mrts_200():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/api/mrts")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 32

@pytest.mark.asyncio
async def test_attractions_200():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/api/attractions")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 12

@pytest.mark.asyncio
async def test_attractions_200_keyword():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/api/attractions?keyword=台北")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 4

@pytest.mark.asyncio
async def test_attractions_422():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/api/attractions?page=-1")
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_attraction_200():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/api/attraction/1")
    assert response.status_code == 200
    assert response.json()["data"]['id'] == 1
    
@pytest.mark.asyncio
async def test_attraction_404():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/api/attraction/99")
    assert response.status_code == 404