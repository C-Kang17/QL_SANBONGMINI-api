from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.config import *
from db.database import get_db
from module.v1.Order import schemas, models, services
from module.v1.Users.routers import get_user_by_ma_kh
from typing import List

router = APIRouter(
    prefix="/module/v1/orders",
    tags=["orders"],
)

def get_order_by_ma_pds(ma_pds: str, db: Session):
    db_order = db.query(models.Order).filter(models.Order.ma_pds == ma_pds).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Phiếu đặt sân với {ma_pds} không tìm thấy!")
    return db_order

@router.get("/all", response_model=List[schemas.OrderResponse])
async def get_all_order(db: Session = Depends(get_db)):
    data_order = db.query(models.Order).all()
    if not data_order:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu đặt sân nào!")
    return data_order

@router.get("/detail", response_model=schemas.OrderResponse)
async def get_detail_order(ma_pds: str, db: Session = Depends(get_db)):
    data_order = get_order_by_ma_pds(ma_pds, db)
    return data_order

@router.post("/create", response_model=schemas.OrderResponse)
async def create_order(data: schemas.OrderRequest, db: Session = Depends(get_db)):
    db_user = get_user_by_ma_kh(data.ma_kh, db)
    ma_pds = services.generate_ma_pds()
    new_order = models.Order(
        ma_pds=ma_pds,
        ma_kh=db_user.ma_kh,
        ghi_chu=data.ghi_chu
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.delete("/{ma_pds}")
async def delete_order(ma_pds: str, db: Session = Depends(get_db)):
    order_to_delete = db.query(models.Order).filter(models.Order.ma_pds == ma_pds).first()
    if not order_to_delete:
        raise HTTPException(status_code=404, detail="Phiếu đặt sân với {ma_pds} không tìm thấy")
    db.delete(order_to_delete)
    db.commit()
    return {"detail": "Xóa phiếu đặt sân thành công"}