from sqlalchemy import Column, CHAR, NVARCHAR, TIMESTAMP, FLOAT
from db.database import Base

class OrderCommodity(Base):
    __tablename__ = "PHIEU_NHAP"

    ma_pn = Column(CHAR(10), primary_key=True, index=True)
    ma_nv = Column(CHAR(10))
    ten_pn = Column(NVARCHAR(20))
    ngay_nhap = Column(TIMESTAMP)
    tong_tien_pn = Column(FLOAT)
