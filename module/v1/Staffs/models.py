from sqlalchemy import Column, String, CHAR,VARCHAR
from db.database import Base

class Staff(Base):
    __tablename__ = "NHAN_VIEN"

    ma_nv = Column(CHAR(10), primary_key=True, index=True)
    ten_nv =   Column(VARCHAR(50)),
    pass_nv =  Column(VARCHAR(100)),
    sdt_nv =   Column(CHAR(11)),
    dia_chi =  Column(VARCHAR(100)),
    email_nv = Column(String(40)),
    chuc_vu =  Column(VARCHAR(30)),
