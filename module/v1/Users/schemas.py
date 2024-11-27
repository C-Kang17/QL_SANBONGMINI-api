from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister (BaseModel):
    pass_kh: str
    ten_kh: str
    sdt_kh: str = None
    email_kh: Optional[EmailStr] 
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    ma_kh: Optional[str] = None
    ten_kh: Optional[str] = None
    sdt_kh: Optional[str] = None 
    email_kh: Optional[str] = None

class UserLogin(BaseModel):
    email_kh: EmailStr
    pass_kh: str

class UserLoginResponse(BaseModel):
    ma_kh: str
    ten_kh: str
    email_kh: str
    sdt_kh: str

class UserEditRequest(BaseModel):
    pass_kh: Optional[str] = None
    ten_kh: Optional[str] = None
    sdt_kh: Optional[str] = None
    class Config:
        orm_mode = True