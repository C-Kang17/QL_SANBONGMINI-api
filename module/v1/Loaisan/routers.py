from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from module.v1.Loaisan import schemas, models, services
from db.config import *
from typing import List

router = APIRouter(
    prefix="/module/v1/loaisan",
    tags=["loaisan"],
)

@router.get("/all", response_model=List[schemas.Response])
async def get_all_loai_san(db: Session = Depends(get_db)):
    data_loai_san = db.query(models.LoaiSan).all()
    if not data_loai_san:
        raise HTTPException(status_code=404, detail="Not found Loai San")
    return data_loai_san