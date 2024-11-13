from sqlalchemy import Column, String, CHAR, NVARCHAR,BLOB
from db.database import Base

class Staff(Base):
    __tablename__ = "NHAN_VIEN"

    ma_nv = Column(CHAR(10), primary_key=True, index=True)
    ten_nv =   Column(NVARCHAR(100))
    pass_nv =  Column(NVARCHAR(150))
    sdt_nv =   Column(NVARCHAR(50))
    dia_chi =  Column(BLOB)
    email_nv = Column(NVARCHAR(100))
    chuc_vu =  Column(NVARCHAR(15))
