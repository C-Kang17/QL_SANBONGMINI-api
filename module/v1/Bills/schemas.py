from pydantic import BaseModel
from datetime import datetime


class Request(BaseModel):
    ma_pds: str
    ma_nv: str
    tong_tien_hd: float
    class Config:
        orm_mode = True

class response(BaseModel):
    ma_hd: str
    ma_pds: str
    ma_nv: str
    ngay_lap: datetime
    tong_tien_hd: str