from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.config import *
from db.database import get_db
from typing import List
from module.v1.Bills import schemas, models, services
from datetime import datetime

from module.v1.Order.routers import get_order_by_ma_pds
from module.v1.Staffs.routers import get_staff_by_ma_nv


router = APIRouter(
    prefix="/module/v1/bill",
    tags=["bills"],
)

def get_bill_by_ma_hd(ma_hd: str, db: Session):
    db_Bill = db.query(models.Bill).filter(models.Bill.ma_hd == ma_hd).first()
    if db_Bill is None:
        raise HTTPException(status_code=404, detail="Hóa đơn với {ma_hd} không tìm thấy!")
    return db_Bill

@router.get("/all", response_model=list[schemas.response])
async def get_all_bills(db: Session = Depends(get_db)):
    bills = db.query(models.Bill).all()
    if not bills:
        raise HTTPException(status_code=404, detail="Không tìm thấy hóa đơn nào")
    
@router.get("detail", response_model=schemas.response)
async def get_detail_bill(ma_hd: str, db: Session = Depends(get_db)):
    data_bill = get_bill_by_ma_hd(ma_hd, db)
    return data_bill

@router.post("/create", response_model=schemas.Request)
async def create_order(data: schemas.Request, db: Session = Depends(get_db)):
    ma_hd = services.generate_ma_hd()
    db_order = get_order_by_ma_pds(data.ma_pds, db)
    if not db_order:
        raise HTTPException(status_code=404, detail="Phiếu đặt sân với {data.ma_pds} không tìm thấy!")
    db_staff = get_staff_by_ma_nv(data.ma_nv, db)
    if not db_staff:
        raise HTTPException(status_code=404, detail="Nhân viên với {data.ma_nv} không tìm thấy!")
    bill = models.Bill(
        ma_hd = ma_hd,
        ma_pds = db_order.ma_pds,
        ma_nv = db_staff.ma_nv,
        ngay_lap = datetime.now(),
        tong_tien_hd = data.tong_tien_hd,
    )
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill