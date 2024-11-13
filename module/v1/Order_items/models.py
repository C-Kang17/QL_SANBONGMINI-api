from sqlalchemy import Column, CHAR, NVARCHAR, DATE, TIMESTAMP, Interval
from db.database import Base

class OrderItem(Base):
    __tablename__ = "CHI_TIET_PDS"

    ma_san = Column(CHAR(10), primary_key=True, index=True)
    ma_pds = Column(CHAR(10), primary_key=True, index=True)
    ngay_dat_san = Column(DATE, nullable=False)
    gio_bd = Column(TIMESTAMP, nullable=False)
    gio_kt = Column(TIMESTAMP, nullable=False)
    ghi_chu = Column(NVARCHAR(30))
