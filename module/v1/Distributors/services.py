import re
from fastapi import HTTPException
from sqlalchemy.orm import Session
from module.v1.Distributors import models
import random

def generate_ma_npp() -> str:
    prefix = "NPP"
    # Tạo 8 chữ số ngẫu nhiên
    random_digits = ''.join([str(random.randint(0, 8)) for _ in range(7)])
    # Ghép tiền tố NPP với chuỗi số ngẫu nhiên
    ma_npp = prefix + random_digits
    return ma_npp


# Kiểm tra định dạng email
def validate_email_format(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    return True


# Kiểm tra email có tồn tại trong cơ sở dữ liệu
def check_existing_email(db: Session, email: str):
    return db.query(models.Distributor).filter(models.Distributor.email_npp == email).first()

# Hàm tính modulo ngược của key
def mod_inverse(key: int, m: int) -> int:
    for i in range(1, m):
        if (key * i) % m == 1:
            return i
    raise ValueError(f"Modular inverse for key {key} does not exist with mod {m}.")

# Hàm mã hóa Caesar phép nhân
def encrypt_multiplicative_caesar(plaintext: str, key: int) -> str:
    result = ""
    for char in plaintext:
        char_code = ord(char)
        encrypted_char_code = (char_code * key) % 256
        result += chr(encrypted_char_code)
    return result

# Hàm giải mã Caesar phép nhân
def decrypt_multiplicative_caesar(ciphertext: str, key: int) -> str:
    result = ""
    mod_inv = mod_inverse(key, 256)
    for char in ciphertext:
        char_code = ord(char)
        decrypted_char_code = (char_code * mod_inv) % 256
        result += chr(decrypted_char_code)
    return result