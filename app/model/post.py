from pydantic import BaseModel, Field

class PresignedUrlRes(BaseModel):
    url : str = Field(..., description = "presigned url")