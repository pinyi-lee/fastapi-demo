from typing import List
from pydantic import BaseModel, Field

class MRTListRes(BaseModel):
	data : List[str] = Field(..., description = "MRT數據列表")