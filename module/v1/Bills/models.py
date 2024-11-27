from sqlalchemy import Column, CHAR, FLOAT, TIMESTAMP
from db.database import Base

class Bill(Base):
    __tablename__ = "HOA_DON"
    ma_hd = Column(CHAR(10), primary_key=True, index=True)
    ma_pds = Column(CHAR(10))
    ma_nv = Column(CHAR(10))
    ngay_lap = Column(TIMESTAMP)
    tong_tien_hd = Column(FLOAT)
