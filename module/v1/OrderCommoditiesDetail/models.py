from sqlalchemy import Column, CHAR, NVARCHAR, DATE, TIMESTAMP, NUMERIC
from db.database import Base

class OrderCommodityDetail(Base):
    __tablename__ = "CHI_TIET_PN"

    ma_pn = Column(CHAR(10), primary_key=True, index=True)
    ma_mh = Column(CHAR(10), primary_key=True, index=True)
    so_luong = Column(NUMERIC)
