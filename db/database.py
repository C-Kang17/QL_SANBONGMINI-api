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

# def create_default_admin(db: Session):
#     admin_id = "ADMIN"
#     admin_email = "admin@gmail.com"  # Địa chỉ email của admin
#     admin_pass = "admin@Admin123"       # Mật khẩu của admin
#     admin_phone = "0123456789"           # Số điện thoại của admin
#     admin_address = "123 Admin Street"   # Địa chỉ của admin
#     admin_role = "admin"                 # Vai trò của admin

#     # Kiểm tra xem tài khoản admin đã tồn tại chưa
#     existing_admin = db.query(models_staff.Staff).filter(models_staff.Staff.email_nv == admin_email).first()
#     if not existing_admin:
#         # Tạo tài khoản admin mới
#         new_admin = models_staff.Staff(

#             ten_nv="Admin",
#             pass_nv=admin_pass,
#             sdt_nv=admin_phone,
#             dia_chi=admin_address,
#             email_nv=admin_email,
#             chuc_vu=admin_role,
#         )
#         db.add(new_admin)
#         db.commit()
#         db.refresh(new_admin)
#         print("Default admin account created.")
#     else:
#         print("Admin account already exists.")