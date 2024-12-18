from sqlalchemy import Column, CHAR, FLOAT, TIMESTAMP, NVARCHAR
from db.database import Base

class Bill(Base):
    __tablename__ = "HOA_DON"
    ma_hd = Column(CHAR(10), primary_key=True, index=True)
    ma_pds = Column(CHAR(10))
    ma_nv = Column(CHAR(10), nullable=True)
    ngay_lap = Column(TIMESTAMP)
    tong_tien_hd = Column(FLOAT)
    hinh_thuc_thanh_toan = Column(NVARCHAR(20))
    han_muc_thanh_toan = Column(NVARCHAR(10))