from sqlalchemy import Column, CHAR, NVARCHAR, DATE, TIMESTAMP, FLOAT
from db.database import Base

class OrderItem(Base):
    __tablename__ = "CHI_TIET_PDS"

    ma_san = Column(CHAR(5), primary_key=True, index=True)
    ma_pds = Column(CHAR(10), primary_key=True, index=True)
    ngay_dat_san = Column(DATE, nullable=False)
    gio_bd = Column(TIMESTAMP, nullable=False)
    gio_kt = Column(TIMESTAMP, nullable=False)
    ghi_chu = Column(NVARCHAR(30))
    gia_san_tong = Column(FLOAT)
    hinh_thuc_thanh_toan = Column(NVARCHAR(20))
    han_muc_thanh_toan = Column(NVARCHAR(10))

