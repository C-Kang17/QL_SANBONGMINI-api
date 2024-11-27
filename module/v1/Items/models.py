from sqlalchemy import Column, CHAR, FLOAT, TIMESTAMP, NVARCHAR
from db.database import Base

class Items(Base):
    __tablename__ = "MAT_HANG"
    ma_mh = Column(CHAR(10), primary_key=True, index=True)
    ma_npp = Column(CHAR(10))
    ten_mh = Column(NVARCHAR(50))
    don_gia_nhap = Column(FLOAT)
    don_gia_ban = Column(FLOAT)
    hinh_anh_mh = Column(NVARCHAR(300))
