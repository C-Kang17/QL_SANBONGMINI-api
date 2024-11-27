from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from module.v1.OrderCommoditiesDetail import schemas, models, services
from module.v1.OrderCommodities import models as models_order_commodity
from module.v1.Items import models as models_item
from datetime import datetime
from db.config import *
from typing import List

router = APIRouter(
    prefix="/module/v1/OrderCommodityDetail",
    tags=["OrderCommoditiesDetail"],
)

@router.get("/all", response_model=List[schemas.Response])
async def get_all_OrderCommoditiesDetail(db: Session = Depends(get_db)):
    data_order = db.query(models.OrderCommodityDetail).all()
    if not data_order:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu nhập nào!")
    return data_order

@router.get("/detail", response_model=schemas.Response)
async def get_order_commodity_detail(ma_pn: str, ma_mh: str, db: Session = Depends(get_db)):
    data_order = db.query(models.OrderCommodityDetail).filter(models.OrderCommodityDetail.ma_pn == ma_pn, models.OrderCommodityDetail.ma_mh == ma_mh).first()
    if not data_order:
        raise HTTPException(status_code=404, detail="Phiếu nhập với mã {ma_pn} và mặt hàng với mã {ma_mh} không tìm thấy!")
    return data_order

@router.post("/create", response_model=schemas.Response)
async def create_order_commodity_detail(data: schemas.Request, db: Session = Depends(get_db)):
    data_order_commodity = db.query(models_order_commodity.OrderCommodity).filter(models_order_commodity.OrderCommodity.ma_pn == data.ma_pn).first()
    if not data_order_commodity:
        raise HTTPException(status_code=404, detail="Phiếu nhập với mã {data.ma_pn} không tìm thấy! ")

    data_item = db.query(models_item.Items).filter(models_item.Items.ma_mh == data.ma_mh).first()
    if not data_item:
        raise HTTPException(status_code=404, detail="Mặt hàng với mã {data.ma_mh} không tìm thấy! ")

    order_commodity_detail = models.OrderCommodityDetail(
        ma_pn=data.ma_pn,
        ma_mh=data.ma_mh,
        so_luong=data.so_luong,
    )

    db.add(order_commodity_detail)
    db.commit()
    db.refresh(order_commodity_detail)

    return order_commodity_detail

@router.delete("/delete", status_code=204)
async def delete_order_item(ma_pn: str, ma_mh: str, db: Session = Depends(get_db)):
    order_item = db.query(models.OrderCommodityDetail).filter(models.OrderCommodityDetail.ma_pn == ma_pn, models.OrderCommodityDetail.ma_mh == ma_mh).first()

    if not order_item:
        raise HTTPException(status_code=404, detail="Phiếu nhập với mã {ma_pn} và mặt hàng với mã {ma_mh} không tìm thấy! ")

    db.delete(order_item)
    db.commit()

    return {"detail": "Xóa chi tiết phiếu nhập thành công"}