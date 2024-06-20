from pydantic import BaseModel, Field

class ServiceError(BaseModel):
    status : int = Field(None)
    error_code : str = Field("error_code")
    error_message : str = Field("error_message")

class BadRequestError(ServiceError):
    status : int = Field(400)
    error_code : str = Field("400-001")
    error_message : str = Field("請求錯誤")

class ForbiddenError(ServiceError):
     status : int = Field(403)
     error_code : str = Field("403-001")
     error_message : str = Field("無權限")

class NotFoundError(ServiceError):
    status : int = Field(404)
    error_code : str = Field("404-001")
    error_message : str = Field("找不到內容")

class InternalServerError(ServiceError):
    status : int = Field(500)
    error_code : str = Field("500-001")
    error_message : str = Field("內部錯誤")

class AttractionIDError(BadRequestError):
    error_code : str = Field("400-002")
    error_message : str = Field("景點編號不正確")

class AttractionNotFoundError(NotFoundError):
    error_code : str = Field("404-002")
    error_message : str = Field("景點找不到")

class DBError(InternalServerError):
    error_code : str = Field("500-002")
    error_message : str = Field("資料庫錯誤")