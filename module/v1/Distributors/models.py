from sqlalchemy import Column, String, CHAR,VARCHAR,BLOB
from db.database import Base

class Distributor(Base):
    __tablename__ = "NHA_PP"
    ma_npp = Column(CHAR(10), primary_key=True, index=True)
    ma_nv = Column(CHAR(10))
    ten_npp = Column(VARCHAR(50))
    dc_npp = Column(BLOB)
    sdt_npp = Column(CHAR(12))
    email_npp = Column(String(50))
