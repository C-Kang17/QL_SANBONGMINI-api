from sqlalchemy import Column, String, CHAR, NVARCHAR, BLOB
from db.database import Base

class User(Base):
    __tablename__ = "KHACH_HANG"

    ma_kh = Column(CHAR(10), primary_key=True, index=True)
    pass_kh = Column(NVARCHAR(150))
    ten_kh = Column(NVARCHAR(100))
    sdt_kh = Column(NVARCHAR(50))
    email_kh = Column(NVARCHAR(100))
    # khuon_mat = Column(BLOB)