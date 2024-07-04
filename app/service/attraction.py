from fastapi import APIRouter, Query, Path
import pickle

from service.cache import get_redis as redis
from service.service import bindResponse
from database.attraction import get_attraction_list as get_attraction_list_from_db
from database.attraction import get_attraction as get_attraction_from_db
from model.attraction import AttractionListRes, AttractionRes
from model.error import ServiceError, AttractionIDError, AttractionNotFoundError, DBError, InternalServerError

router = APIRouter()

@router.get("/api/attractions",
            summary = "取得景點資料列表",
            description="取得不同分頁的旅遊景點列表資料，也可以根據標題關鍵字、或捷運站名稱篩選",
    response_model = AttractionListRes,
    responses = {
        200: {"description": "成功取得景點資料", "model": AttractionListRes},
        500: {"description": "伺服器內部錯誤", "model": DBError},
    })
async def get_attraction_list(
    page: int = Query(0, ge=0 , description = "要取得的分頁，每頁 12 筆資料" ),
    keyword: str = Query(None, description = "用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選")
) -> AttractionListRes | ServiceError:
    try:
        cache_key = f'attraction_list:{page}:{keyword}'
        cached_data = redis().get(cache_key)
        if cached_data:
            return bindResponse(pickle.loads(cached_data))
        data = get_attraction_list_from_db(page, keyword)
        redis().setex(cache_key, 3600, pickle.dumps(data))
        return bindResponse(data)
        
    except Exception as e:
        print("get attraction list serivce error, error message:" , e)
        return bindResponse(InternalServerError())

@router.get("/api/attraction/{attractionId}",
    summary = "根據景點編號取得景點資料",
    description="根據景點編號取得景點資料",
    response_model = AttractionRes,
    responses = {
        200: {"description": "成功取得景點資料", "model": AttractionRes},
        400: {"description": "錯誤的請求", "model": AttractionIDError},
        404: {"description": "找不到該景點", "model": AttractionNotFoundError},
        500: {"description": "伺服器內部錯誤", "model": DBError},
    })
async def get_attraction(   
    attractionId: int = Path(..., description = "景點編號")
) -> AttractionRes | ServiceError:
    try:
        cache_key = f'attraction:{attractionId}'
        cached_data = redis().get(cache_key)
        if cached_data:
            return bindResponse(AttractionRes(data = pickle.loads(cached_data)))
            
        data = get_attraction_from_db(attractionId)
        if isinstance(data, ServiceError):
            return bindResponse(data)
        
        redis().setex(cache_key, 3600, pickle.dumps(data))
        return bindResponse(AttractionRes(data = data))
        
    except Exception as e:
        print("get attraction serivce error, error message:" , e)
        return bindResponse(InternalServerError())