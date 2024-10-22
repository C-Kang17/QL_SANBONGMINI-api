from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from module.v1.Distributors import schemas, models, services
from module.v1.Staffs import models as models_staff
from db.config import *
from module.v1.Distributors.config import *
from utils.callfunction import *

router = APIRouter(
    prefix="/mudule/v1/distributor",
    tags=["distributors"],
)

@router.get("/all", response_model=list[schemas.DistributorResponse])
def get_all_distributors(db: Session = Depends(get_db)):
    distributors = db.query(models.Distributor).all()
    if not distributors:
        raise HTTPException(status_code=404, detail="No distributors found")
    return distributors

@router.post("/register", response_model=schemas.DistributorResponse)
def create_distributor(distributor: schemas.DistributorRegister, db: Session = Depends(get_db)):
    db_staff = db.query(models_staff.Staff).filter(models_staff.Staff.ma_nv == distributor.ma_nv).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Invalid 'Mã Nhân viên'")
    
    ma_npp = services.generate_ma_npp()
    db_distributor = db.query(models.Distributor).filter(models.Distributor.ma_npp == ma_npp).first()
    if db_distributor:
        raise HTTPException(status_code=400, detail="distributor already registered")
    encrypt_email=encrypt_caesar(distributor.email_npp, key)
    services.validate_email_format(distributor.email_npp)
    db_distributor = services.check_existing_email(db, encrypt_email)
    if db_distributor:
        raise HTTPException(status_code=400, detail="Email distributor already registered")
    encrypt_name = encrypt_caesar(distributor.ten_npp,key)
    encrypt_location  = encrypt_des(distributor.dc_npp, key_des)
    encrypt_phone = encrypt_caesar(distributor.sdt_npp, key)
    
    db_distributor = models.Distributor(
        ma_npp = ma_npp,
        ma_nv = distributor.ma_nv,
        ten_npp = encrypt_name,
        dc_npp = encrypt_location,
        sdt_npp = encrypt_phone,
        email_npp = encrypt_email
    )
    db.add(db_distributor)
    db.commit()
    db.refresh(db_distributor)
    return db_distributor

@router.put("/edit/{ma_npp}", response_model=schemas.DistributorResponse)
def edit_distributor(ma_npp: str, distributor: schemas.DistributorEditRequest, db: Session = Depends(get_db)):
    db_distributor = db.query(models.Distributor).filter(models.Distributor.ma_npp == ma_npp).first()
    if db_distributor is None:
        raise HTTPException(status_code=404, detail="Distributor not found")
    data = distributor.model_dump(exclude_none=True)
    if not any(getattr(db_distributor, k) != value for k, value in data.items()):
        raise HTTPException(status_code=304, detail="No modifications")
    
    if data.get("dc_npp"):
        encrypt_location  = encrypt_des(distributor.dc_npp, key_des)
        data["dc_npp"] = encrypt_location
    if data.get("sdt_npp"):
        encrypt_phone = encrypt_caesar(data["sdt_npp"], key)
        data["sdt_npp"] = encrypt_phone
    if data.get("email_npp"):
        encrypt_email=encrypt_caesar(data["email_npp"], key)
        data["email_npp"] = encrypt_email

    for k, value in data.items():
        setattr(db_distributor, k, value)

    db.commit()
    db.refresh(db_distributor)
    return db_distributor

@router.delete("/delete/{ma_npp}", response_model=dict)
def delete_distributor(ma_npp: str, db: Session = Depends(get_db)):
    db_distributor = db.query(models.Distributor).filter(models.Distributor.ma_npp == ma_npp).first()
    if db_distributor is None:
        raise HTTPException(status_code=404, detail="Distributor not found")

    db.delete(db_distributor)
    db.commit()
    
    return {"detail": "Distributor deleted successfully"}