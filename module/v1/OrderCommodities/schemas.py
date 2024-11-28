from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Request(BaseModel):
    ma_nv: str
    ten_pn: str
    tong_tien_pn: float

    class Config:
        orm_mode = True

class Response (BaseModel):
    ma_pn: str
    ma_nv: str
    ten_pn: str
    ngay_nhap: datetime
    tong_tien_pn: float