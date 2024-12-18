from sqlalchemy import Column, CHAR, NVARCHAR
from db.database import Base

class User(Base):
    __tablename__ = "KHACH_HANG"

    ma_kh = Column(CHAR(10), primary_key=True, index=True)
    pass_kh = Column(NVARCHAR(1000))
    ten_kh = Column(NVARCHAR(100))
    sdt_kh = Column(NVARCHAR(50))
    email_kh = Column(NVARCHAR(200))