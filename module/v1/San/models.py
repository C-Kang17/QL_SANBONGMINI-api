from sqlalchemy import Column, CHAR, NVARCHAR
from db.database import Base

class San(Base):
    __tablename__ = "SAN"

    ma_san = Column(CHAR(5), primary_key=True, index=True)
    ten_san = Column(NVARCHAR(20))
    tinh_trang = Column(NVARCHAR(10)) 