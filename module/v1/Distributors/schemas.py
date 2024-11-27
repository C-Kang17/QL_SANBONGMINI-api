from pydantic import BaseModel, EmailStr
from typing import Optional

class DistributorRegister (BaseModel):
    ten_npp: str
    dc_npp: str = None
    sdt_npp: str 
    email_npp: Optional[EmailStr]
    class Config:
        orm_mode = True

class DistributorResponse(BaseModel):
    ma_npp: Optional[str] = None
    ten_npp: Optional[str] = None
    dc_npp: Optional[str] = None
    sdt_npp: Optional[str] = None
    email_npp: Optional[str] = None


class DistributorEditRequest (BaseModel):
    ten_npp: Optional[str] = None
    dc_npp: Optional[str] = None
    sdt_npp: Optional[str] = None 
    email_npp: Optional[EmailStr] = None
    class Config:
        orm_mode = True