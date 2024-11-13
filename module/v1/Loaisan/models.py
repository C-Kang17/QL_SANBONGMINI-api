from sqlalchemy import Column, CHAR, FLOAT, NVARCHAR
from db.database import Base

class LoaiSan(Base):
    __tablename__ = "LOAI_SAN"

    ma_ls = Column(CHAR(5), primary_key=True, index=True)
    ma_san = Column(CHAR(10), primary_key=True, index=True)
    loai_mat_co = Column(NVARCHAR(30))
    kich_thuoc_san = Column(CHAR(10))
    gia_san = Column(FLOAT)