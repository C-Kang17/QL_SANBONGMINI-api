from pydantic import BaseModel
from typing import Optional
from datetime import date, timedelta

class OrderRequest (BaseModel):
    ma_kh: str
    ghi_chu: Optional[str] = None
    class Config:
        orm_mode = True

class OrderResponse (BaseModel):
    ma_pds: str
    ma_kh: str
    ghi_chu: Optional[str] = None