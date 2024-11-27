import random

def generate_ma_pn() -> str:
    prefix = "PN"
    # Tạo 8 chữ số ngẫu nhiên
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    # Ghép tiền tố PN với chuỗi số ngẫu nhiên
    ma_pn = prefix + random_digits
    return ma_pn