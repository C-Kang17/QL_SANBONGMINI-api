from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Request(BaseModel):
    ma_pn: str
    ma_mh: str
    so_luong: int

    class Config:
        orm_mode = True

class Response(BaseModel):
    ma_pn: str
    ma_mh: str
    so_luong: int

class Edit(BaseModel):
    so_luong: Optional[int] = None

    class Config:
        orm_mode = True
