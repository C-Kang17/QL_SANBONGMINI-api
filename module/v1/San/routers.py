from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from utils.callfunction import encrypt_caesar, encrypt_des
from module.v1.San import schemas, models, services
from db.config import *
from typing import List

router = APIRouter(
    prefix="/module/v1/san",
    tags=["san"],
)

@router.get("/all", response_model=List[schemas.Response])
async def get_all_san(db: Session = Depends(get_db)):
    data_san = db.query(models.San).all()
    if not data_san:
        raise HTTPException(status_code=404, detail="Not found San")
    return data_san

@router.put("/{ma_san}", response_model=schemas.Response)
async def edit_san(ma_san: str, data: schemas.EditSanRequest, db: Session = Depends(get_db)):
    san_record = db.query(models.San).filter(models.San.ma_san == ma_san).first()
    if not san_record:
        raise HTTPException(status_code=404, detail="Not found ma_san")
    if data.tinh_trang is not None:
        san_record.tinh_trang = data.tinh_trang
    db.commit()
    db.refresh(san_record)
    return san_record