from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Request(BaseModel):
    ma_pds: str
    ma_nv: Optional[str] = None
    tong_tien_hd: float
    hinh_thuc_thanh_toan: str
    han_muc_thanh_toan: str
    
    class Config:
        orm_mode = True

class response(BaseModel):
    ma_hd: str
    ma_pds: str
    ma_nv: Optional[str] = None
    ngay_lap: datetime
    tong_tien_hd: str
    hinh_thuc_thanh_toan: str
    han_muc_thanh_toan: str

    