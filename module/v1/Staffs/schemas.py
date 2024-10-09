from pydantic import BaseModel, EmailStr
from typing import Optional

class StaffRegister (BaseModel):
    ten_nv: str
    pass_nv: str
    sdt_nv: str
    dia_chi: str
    email_nv: Optional[EmailStr] 
    chuc_vu: str
    class Config:
        orm_mode = True

class StaffRegisterResponse(BaseModel):
    ma_nv: str
    ten_nv: str
    pass_nv: str
    sdt_nv: str
    dia_chi: str
    email_nv: Optional[EmailStr] 
    chuc_vu: str

class StaffLogin(BaseModel):
    email_nv: str
    pass_nv: str

class StaffLoginResponse(BaseModel):
    chuc_vu: str