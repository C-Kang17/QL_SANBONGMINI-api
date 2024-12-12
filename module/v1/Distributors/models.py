from sqlalchemy import Column, CHAR, NVARCHAR,BLOB
from db.database import Base

class Distributor(Base):
    __tablename__ = "NHA_PP"
    ma_npp = Column(CHAR(10), primary_key=True, index=True)
    ten_npp = Column(NVARCHAR(100))
    dc_npp = Column(BLOB)
    sdt_npp = Column(NVARCHAR(1000))
    email_npp = Column(NVARCHAR(200))
