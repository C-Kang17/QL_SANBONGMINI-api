import re
from fastapi import HTTPException
from sqlalchemy.orm import Session
from module.v1.Users import models
import random

def generate_ma_kh() -> str:
    prefix = "KH"
    # Tạo 8 chữ số ngẫu nhiên
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    # Ghép tiền tố KH với chuỗi số ngẫu nhiên
    ma_kh = prefix + random_digits
    return ma_kh

def check_password_length(password: str) -> bool:
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    return True

# Kiểm tra mật khẩu
def verify_password(input_password: str, stored_password: str) -> bool:
    return input_password == stored_password


# Kiểm tra định dạng email
def validate_email_format(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    return True


# Kiểm tra email có tồn tại trong cơ sở dữ liệu
def check_existing_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email_kh == email).first()
