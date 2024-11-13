from sqlalchemy import Column, String, CHAR, NVARCHAR,BLOB
from db.database import Base

class Distributor(Base):
    __tablename__ = "NHA_PP"
    ma_npp = Column(CHAR(10), primary_key=True, index=True)
    ma_nv = Column(CHAR(10))
    ten_npp = Column(NVARCHAR(100))
    dc_npp = Column(BLOB)
    sdt_npp = Column(NVARCHAR(50))
    email_npp = Column(NVARCHAR(100))
