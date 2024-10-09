from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from db.config import DB_HOST
import os

# Thay đổi các thông tin kết nối phù hợp với cấu hình

DATABASE_URL = f"oracle+cx_oracle://QL_SANBONGMINI:123@{DB_HOST}:1521/orcl2"

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
