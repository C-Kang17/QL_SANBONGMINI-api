from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.config import *
from db.database import get_db
from typing import List
from module.v1.Items import schemas, models, services
from datetime import datetime

from module.v1.Distributors.routers import get_distributor_by_ma_npp

router = APIRouter(
    prefix="/module/v1/Item",
    tags=["Items"],
)

def get_item_by_ma_mh(ma_mh: str, db: Session):
    db_Item = db.query(models.Items).filter(models.Items.ma_mh == ma_mh).first()
    if db_Item is None:
        raise HTTPException(status_code=404, detail="Mặt hàng với mã {ma_mh} và không tìm thấy mặt hàng!")
    return db_Item

@router.get("/all", response_model=List[schemas.response])
async def get_all_items(db: Session = Depends(get_db)):
    items = db.query(models.Items).all()
    if not items:
        raise HTTPException(status_code=404, detail="Không tìm thấy mặt hàng nào")
    return items

@router.get("detail", response_model=schemas.response)
async def get_detail_item(ma_mh: str, db: Session = Depends(get_db)):
    data_item = get_item_by_ma_mh(ma_mh, db)
    return data_item

@router.post("/add", response_model=schemas.Request)
async def add_item(data: schemas.Request, db: Session = Depends(get_db)):
    ma_mh = services.generate_ma_mh()

    db_distributor = get_distributor_by_ma_npp(data.ma_npp, db)
    if not db_distributor:
        raise HTTPException(status_code=404, detail="Nhà phân phối với {data.ma_npp} không tìm thấy!")
    
    item = models.Items(
        ma_mh = ma_mh,
        ma_npp = data.ma_npp,
        ten_mh = data.ten_mh,
        don_gia_nhap = data.don_gia_nhap,
        don_gia_ban = data.don_gia_ban,
        hinh_anh_mh = data.hinh_anh_mh,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/edit", response_model=schemas.response)
def edit_item(ma_mh: str, item: schemas.edit, db: Session = Depends(get_db)):
    db_item = get_item_by_ma_mh(ma_mh, db)
    data = item.model_dump(exclude_none=True)
    if not any(getattr(db_item, k) != v for k, v in data.items()):
        raise HTTPException(status_code=304, detail="No modifications")

    for key_chk, value in data.items():
        setattr(db_item, key_chk, value)

    db.commit()
    db.refresh(db_item)
    return db_item