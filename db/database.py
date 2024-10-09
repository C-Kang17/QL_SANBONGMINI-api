from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from db.config import *
import os

# Thay đổi các thông tin kết nối phù hợp với cấu hình

DATABASE_URL = f"oracle+cx_oracle://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_SID}"

engine = create_engine(DATABASE_URL, echo=True)

# Tạo session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model cho các class ORM
Base = declarative_base()

# Dependency để sử dụng session trong các route
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
