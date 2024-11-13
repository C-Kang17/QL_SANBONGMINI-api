from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from utils.callfunction import encrypt_caesar, encrypt_des
from module.v1.Order_items import schemas, models, services
from module.v1.Order import models as models_order
from module.v1.San import models as models_san
from datetime import datetime
from db.config import *

router = APIRouter(
    prefix="/module/v1/order-items",
    tags=["order-items"],
)

@router.post("/create", response_model=schemas.Response)
async def create_order_item(data: schemas.OrderItemRequest, db: Session = Depends(get_db)):
    order_item = db.query(models_order.Order).filter(models_order.Order.ma_pds == data.ma_pds).first()
    if not order_item:
        raise HTTPException(status_code=404, detail="The {data.ma_pds} is not found")

    San = db.query(models_san.San).filter(models_san.San.ma_san == data.ma_san).first()
    if not San:
        raise HTTPException(status_code=404, detail="The {data.ma_san} is not found")
    
    ngay_dat_san = data.ngay_dat_san
    if ngay_dat_san is None:
        raise HTTPException(status_code=400, detail="Nhập ngày đặt sân")
    
    ngay_hien_tai = datetime.now().date().strftime("%Y-%m-%d")
    if ngay_dat_san.strftime("%Y-%m-%d") < ngay_hien_tai:
        raise HTTPException(status_code=400, detail="Ngày đặt sân phải lớn hơn hoặc bằng ngày hiện tại")

    gio_bd = data.gio_bd
    if gio_bd is None:
        raise HTTPException(status_code=400, detail="Nhập giờ đặt sân đặt sân")

    if gio_bd >= data.gio_kt:
        raise HTTPException(status_code=400, detail="Giờ bắt đầu phải bé hơn giờ kết thúc")

    order_item = models.OrderItem(
        ma_san=data.ma_san,
        ma_pds=data.ma_pds,
        ngay_dat_san=data.ngay_dat_san,
        gio_bd=data.gio_bd,
        gio_kt=data.gio_kt,
        ghi_chu=data.ghi_chu
    )

    db.add(order_item)
    db.commit()
    db.refresh(order_item)

    return order_item

@router.delete("/delete", status_code=204)
async def delete_order_item(ma_san: str, ma_pds: str, db: Session = Depends(get_db)):
    order_item = db.query(models.OrderItem).filter(
        models.OrderItem.ma_san == ma_san,
        models.OrderItem.ma_pds == ma_pds
    ).first()

    if not order_item:
        raise HTTPException(status_code=404, detail="The {ma_san} and {ma_pds} not found")

    db.delete(order_item)
    db.commit()

    return {"detail": "Order item deleted successfully"}