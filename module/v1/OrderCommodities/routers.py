from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.config import *
from db.database import get_db
from module.v1.OrderCommodities import schemas, models, services
from module.v1.Staffs.routers import get_staff_by_ma_nv
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/module/v1/order_commodity",
    tags=["order_commodities"],
)

def get_order_commodity_by_ma_pn(ma_pn: str, db: Session):
    db_order_commodity = db.query(models.OrderCommodity).filter(models.OrderCommodity.ma_pn == ma_pn).first()
    if db_order_commodity is None:
        raise HTTPException(status_code=404, detail="Phiếu đặt sân với {ma_pn} không tìm thấy!")
    return db_order_commodity

@router.get("/all", response_model=List[schemas.Response])
async def get_all_order_commodities(db: Session = Depends(get_db)):
    db_order_commodities = db.query(models.OrderCommodity).all()
    if not db_order_commodities:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu nhập nào!")
    return db_order_commodities

@router.get("/detail", response_model=schemas.Response)
async def get_detail_order_commodity(ma_pn: str, db: Session = Depends(get_db)):
    data_order = get_order_commodity_by_ma_pn(ma_pn, db)
    return data_order

@router.post("/create", response_model=schemas.Response)
async def create_order_commodity(data: schemas.Request, db: Session = Depends(get_db)):
    db_staff = get_staff_by_ma_nv(data.ma_nv, db)
    ma_pn = services.generate_ma_pn()
    new_order = models.OrderCommodity(
        ma_pn = ma_pn,
        ma_nv = data.ma_nv,
        ten_pn = data.ten_pn,
        ngay_nhap = datetime.now(),
        tong_tien_pn = data.tong_tien_pn,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.delete("/{ma_pn}")
async def delete_order(ma_pn: str, db: Session = Depends(get_db)):
    order_to_delete = db.query(models.OrderCommodity).filter(models.OrderCommodity.ma_pn == ma_pn).first()
    if not order_to_delete:
        raise HTTPException(status_code=404, detail="Phiếu nhập với mã {ma_pn} không tìm thấy")
    db.delete(order_to_delete)
    db.commit()
    return {"detail": "Xóa phiếu nhập thành công"}