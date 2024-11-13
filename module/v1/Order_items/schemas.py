from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderItemRequest(BaseModel):
    ma_san: str
    ma_pds: str
    ngay_dat_san: datetime
    gio_bd: datetime
    gio_kt: datetime
    ghi_chu: Optional[str] = None

    class Config:
        orm_mode = True

class Response(BaseModel):
    ma_san: str
    ma_pds: str
    ngay_dat_san: datetime
    gio_bd: datetime
    gio_kt: datetime
    ghi_chu: Optional[str] = None

class EditOrderItem(BaseModel):
    ngay_dat_san: Optional[str] = None
    gio_bd: Optional[str] = None
    gio_kt: Optional[str] = None
    ghi_chu: Optional[str] = None

    class Config:
        orm_mode = True
