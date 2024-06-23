from fastapi import APIRouter, status
import pickle

from service.cache import get_redis as redis
from service.service import bindResponse
from database.mrt import get_mrt_list as get_mrt_list_from_db
from model.mrt import MRTListRes
from model.error import ServiceError, DBError, InternalServerError

router = APIRouter()

@router.get("/api/mrts",
            summary = "取得捷運站名稱列表",
            description="取得所有捷運站名稱列表，按照週邊景點的數量由大到小排序",
    response_model = MRTListRes,
    responses = {
        200: {"description": "成功取得景點資料", "model": MRTListRes},
        500: {"description": "伺服器內部錯誤", "model": DBError},
    })
async def get_mrt_list() -> MRTListRes | ServiceError:
    try:
        cache_key = f'mrt_list'
        cached_data = redis().get(cache_key)
        if cached_data:
            return bindResponse(MRTListRes(data =pickle.loads(cached_data)))
        data = get_mrt_list_from_db()
        redis().setex(cache_key, 3600, pickle.dumps(data))
        return bindResponse(MRTListRes(data = data))
        
    except Exception as e:
        print("get mrt list serivce error, error message:" , e)
        return bindResponse(InternalServerError())