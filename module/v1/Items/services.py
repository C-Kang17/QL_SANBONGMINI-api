
import random

def generate_ma_mh() -> str:
    prefix = "MH"
    # Tạo 8 chữ số ngẫu nhiên
    random_digits = ''.join([str(random.randint(0, 8)) for _ in range(3)])
    # Ghép tiền tố HD với chuỗi số ngẫu nhiên
    ma_hd = prefix + random_digits
    return ma_hd