import re
from fastapi import HTTPException
from sqlalchemy.orm import Session
from module.v1.Bills import models
import random

def generate_ma_hd() -> str:
    prefix = "HD"
    # Tạo 8 chữ số ngẫu nhiên
    random_digits = ''.join([str(random.randint(0, 8)) for _ in range(7)])
    # Ghép tiền tố HD với chuỗi số ngẫu nhiên
    ma_hd = prefix + random_digits
    return ma_hd