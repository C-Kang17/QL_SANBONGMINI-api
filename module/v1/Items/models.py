from sqlalchemy import Column, CHAR, FLOAT, TIMESTAMP, NVARCHAR
from db.database import Base

class Items(Base):
    __tablename__ = "MAT_HANG"
    ma_mh = Column(CHAR(5), primary_key=True, index=True)
    ma_npp = Column(CHAR(10), nullable=True)
    ten_mh = Column(NVARCHAR(50), nullable=True)
    don_gia_nhap = Column(FLOAT, nullable=True)
    don_gia_ban = Column(FLOAT, nullable=True)
    hinh_anh_mh = Column(NVARCHAR(300), nullable=True)
