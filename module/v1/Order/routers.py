from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from utils.callfunction import encrypt_caesar, encrypt_des
from module.v1.Order import schemas, models, services
from module.v1.Users.routers import get_user_by_ma_kh
from db.config import *

router = APIRouter(
    prefix="/module/v1/orders",
    tags=["orders"],
)

@router.post("/create", response_model=schemas.OrderResponse)
async def create_order(data: schemas.OrderRequest, db: Session = Depends(get_db)):
    db_user = get_user_by_ma_kh(data.ma_kh, db)
    ma_pds = services.generate_ma_pds()
    new_order = models.Order(
        ma_pds=ma_pds,
        ma_kh=data.ma_kh,
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
        raise HTTPException(status_code=404, detail="The {ma_pds} not found")
    db.delete(order_to_delete)
    db.commit()
    return {"detail": "Order deleted successfully"}