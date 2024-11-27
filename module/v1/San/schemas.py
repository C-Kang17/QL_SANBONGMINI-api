from pydantic import BaseModel
from typing import Optional

class Response(BaseModel):
    ma_san: str
    ten_san: str
    tinh_trang: str

class EditSanRequest(BaseModel):
    tinh_trang: Optional[str] 