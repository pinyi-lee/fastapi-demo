from typing import List, Optional
from pydantic import BaseModel, Field

class Attraction(BaseModel):
    id: int = Field(... , example=10)
    name: str = Field(... , example="平安鐘")
    category: str = Field(... , example="公共藝術")
    description: str = Field(... , example="平安鐘祈求大家的平安，這是為了紀念 921 地震週年的設計")
    address: str = Field(... , example="臺北市大安區忠孝東路 4 段 1 號")
    transport: str = Field(... , example="公車：204、212、212直")
    mrt: str = Field(... , example="忠孝復興")
    lat: float = Field(... , example=25.04181)
    lng: float = Field(... , example=121.544814)
    images: List[str] = Field(..., example=["http://140.112.3.4/images/92-0.jpg"])

class AttractionRes(BaseModel):
    data : Attraction = Field(..., description = "景點數據")

class AttractionListRes(BaseModel):
	nextPage : Optional[int]= Field(None, example=2, description = "下一頁的頁碼，若無更多頁面則為 Null")
	data : List[Attraction] = Field(..., description = "景點數據列表")