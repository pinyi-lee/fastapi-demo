from fastapi import status
from fastapi.responses import JSONResponse

from model.error import ServiceError

def bindResponse(data):

    if not isinstance(data, ServiceError):
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = data.dict()
        )
    
    return JSONResponse(
        status_code = data.status,
        content= data.dict()
    )