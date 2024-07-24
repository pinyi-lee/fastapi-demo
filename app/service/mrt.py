from fastapi import APIRouter, status
import pickle

from app.service.cache import RedisManager
from app.service.service import bindResponse
from app.database.mrt import get_mrt_list as get_mrt_list_from_db
from app.model.mrt import MRTListRes
from app.model.error import ServiceError, DBError, InternalServerError
from app.util.logger import LoggerManager

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
        cached_data = RedisManager.get_redis().get(cache_key)
        if cached_data:
            return bindResponse(MRTListRes(data =pickle.loads(cached_data)))
        
        data = get_mrt_list_from_db()

        ## 如果 error 要不存
        RedisManager.get_redis().setex(cache_key, 3600, pickle.dumps(data))
        return bindResponse(MRTListRes(data = data))
        
    except Exception as e:
        LoggerManager.error("get mrt list serivce error, error message:" , e)
        return bindResponse(InternalServerError())