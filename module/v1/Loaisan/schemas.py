from pydantic import BaseModel


class Response(BaseModel):
    ma_ls: str
    ma_san: str
    loai_mat_co: str
    kich_thuoc_san: str
    gia_san: float
