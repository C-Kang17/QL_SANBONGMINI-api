from sqlalchemy.orm import Session
from module.v1.OrderCommodities import models

import random

def generate_ma_pn() -> str:
    prefix = "PN"
    # Tạo 8 chữ số ngẫu nhiên
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    # Ghép tiền tố PN với chuỗi số ngẫu nhiên
    ma_pn = prefix + random_digits
    return ma_pn


def generate_ten_pn(db: Session) -> str:
    existing_order_names = db.query(models.OrderCommodity.ten_pn).all()
    existing_names = [order_name[0] for order_name in existing_order_names]
    base_name = "Phiếu nhập"
    index = 1
    new_name = f"{base_name} {index}"
    while new_name in existing_names:
        index += 1
        new_name = f"{base_name} {index}"
    return new_name