from pydantic import BaseModel
from typing import Optional
from datetime import date, timedelta

class Response(BaseModel):
    ma_san: str
    ten_san: str
    tinh_trang: str

class EditSanRequest(BaseModel):
    tinh_trang: Optional[str] 