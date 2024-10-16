from pydantic import BaseModel ,EmailStr 
from typing import Optional, Literal

class StaffRegister (BaseModel):
    ten_nv: str
    pass_nv: str
    sdt_nv: str
    dia_chi: str
    email_nv: Optional[EmailStr] 
    chuc_vu: Literal["admin", "thu-ngan", "nhap-hang", "nhan-vien"]
    class Config:
        orm_mode = True

class StaffResponse(BaseModel):
    ma_nv: str = None
    ten_nv: str = None
    pass_nv: str = None
    sdt_nv: str = None
    dia_chi: str = None
    email_nv: str = None 
    chuc_vu: str = None

class StaffLogin(BaseModel):
    ma_nv: str
    pass_nv: str

class StaffLoginResponse(BaseModel):
    chuc_vu: str

class StaffEditRequest(BaseModel):
    ten_nv: Optional[str] = None
    pass_nv: Optional[str] = None
    sdt_nv: Optional[str] = None
    dia_chi: Optional[str] = None
    email_nv: Optional[EmailStr] = None 
    chuc_vu: Optional[Literal["admin", "thu-ngan", "nhap-hang", "nhan-vien"]] = None
    class Config:
        orm_mode = True