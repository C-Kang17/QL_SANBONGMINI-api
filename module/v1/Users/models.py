from sqlalchemy import Column, String, CHAR, VARCHAR, BLOB
from db.database import Base

class User(Base):
    __tablename__ = "KHACH_HANG"

    ma_kh = Column(CHAR(10), primary_key=True, index=True)
    pass_kh = Column(VARCHAR(100))
    ten_kh = Column(VARCHAR(50))
    sdt_kh = Column(CHAR(11))
    email_kh = Column(String(50))
    khuon_mat = Column(BLOB)