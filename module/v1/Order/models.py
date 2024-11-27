from sqlalchemy import Column, CHAR, NVARCHAR
from db.database import Base

class Order(Base):
    __tablename__ = "PHIEU_DAT_SAN"

    ma_pds = Column(CHAR(10), primary_key=True, index=True)
    ma_kh = Column(CHAR(10))
    ghi_chu = Column(NVARCHAR(50))