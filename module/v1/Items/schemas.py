from pydantic import BaseModel, Field
from typing import Optional

class Request(BaseModel):
    ma_npp: str
    ten_mh: str
    don_gia_nhap: float = Field(..., gte=0, description="Đơn giá nhập phải lớn hơn 0")
    don_gia_ban: float = Field(..., gte=0, description="Đơn giá bán phải lớn hơn 0")
    hinh_anh_mh: Optional[str] = None
    class Config:
        orm_mode = True

class response(BaseModel):
    ma_mh: str
    ma_npp: str
    ten_mh: str
    don_gia_nhap: float
    don_gia_ban: float
    hinh_anh_mh: Optional[str] = None

class edit(BaseModel):
    ten_mh: Optional[str] = None
    don_gia_nhap: Optional[float] = Field(..., gte=0, description="Đơn giá nhập phải lớn hơn 0")
    don_gia_ban: Optional[float] = Field(..., gte=0, description="Đơn giá bán phải lớn hơn 0")
    hinh_anh_mh: Optional[str] = None