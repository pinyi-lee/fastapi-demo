from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

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
        res = get_mrt_list_from_db()
        if isinstance(res, ServiceError):
            return bindResponse(res)

        return bindResponse(MRTListRes(data = res,))
        
    except Exception as e:
        print("get mrt list serivce error, error message:" , e)
        return bindResponse(InternalServerError())