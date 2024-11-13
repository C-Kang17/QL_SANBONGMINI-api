import re
from fastapi import HTTPException
from sqlalchemy.orm import Session
from module.v1.Order import models
import random

def generate_ma_pds() -> str:
    prefix = "PDS"
    # Tạo 7 chữ số ngẫu nhiên
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    # Ghép tiền tố PDS với chuỗi số ngẫu nhiên
    ma_pds = prefix + random_digits
    return ma_pds