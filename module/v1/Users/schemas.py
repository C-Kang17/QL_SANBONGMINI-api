from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister (BaseModel):
    pass_kh: str
    ten_kh: str
    sdt_kh: str = None
    email_kh: Optional[EmailStr] 

    class Config:
        orm_mode = True

class UserRegisterResponse(BaseModel):
    ma_kh: str
    pass_kh: str
    ten_kh: str
    sdt_kh: str = None
    email_kh: Optional[EmailStr] 

class UserLogin(BaseModel):
    email_kh: str
    pass_kh: str

class UserLoginResponse(BaseModel):
    email_kh: str