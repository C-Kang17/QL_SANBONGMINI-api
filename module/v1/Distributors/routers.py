from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from module.v1.Distributors import schemas, models, services
from module.v1.Staffs import models as models_staff
from utils import callfunction as call_function_services
from db.config import *

router = APIRouter(
    prefix="/module/v1/distributor",
    tags=["distributors"],
)

# Utility function to get distributor by `ma_npp`
def get_distributor_by_ma_npp(ma_npp: str, db: Session):
    db_distributor = db.query(models.Distributor).filter(models.Distributor.ma_npp == ma_npp).first()
    if db_distributor is None:
        raise HTTPException(status_code=404, detail="Distributor not found")
    return db_distributor

@router.get("/all", response_model=list[schemas.DistributorResponse])
def get_all_distributors(db: Session = Depends(get_db)):
    distributors = db.query(models.Distributor).all()
    if not distributors:
        raise HTTPException(status_code=404, detail="No distributors found")
    return distributors

@router.post("/register", response_model=schemas.DistributorResponse, status_code=200)
def create_distributor(distributor: schemas.DistributorRegister, db: Session = Depends(get_db)):
    # Validate staff existence
    db_staff = db.query(models_staff.Staff).filter(models_staff.Staff.ma_nv == distributor.ma_nv).first()
    if not db_staff:
        raise HTTPException(status_code=404, detail="Invalid 'Mã Nhân viên'")

    # Generate unique `ma_npp`
    ma_npp = services.generate_ma_npp()
    if db.query(models.Distributor).filter(models.Distributor.ma_npp == ma_npp).first():
        raise HTTPException(status_code=400, detail="Distributor already registered")

    # Validate and encrypt email
    services.validate_email_format(distributor.email_npp)
    encrypt_email = call_function_services.encrypt_rsa(distributor.email_npp, public_key_rsa)
    if services.check_existing_email(db, encrypt_email):
        raise HTTPException(status_code=400, detail="Email distributor already registered")

    # Encrypt other fields
    encrypt_location = call_function_services.encrypt_des(distributor.dc_npp, key_des)
    encrypt_phone = call_function_services.encrypt_caesar(distributor.sdt_npp, key)

    # Create new distributor entry
    db_distributor = models.Distributor(
        ma_npp=ma_npp,
        ma_nv=distributor.ma_nv,
        ten_npp=distributor.ten_npp,
        dc_npp=encrypt_location,
        sdt_npp=encrypt_phone,
        email_npp=encrypt_email
    )
    db.add(db_distributor)
    db.commit()
    db.refresh(db_distributor)
    return db_distributor

@router.put("/edit/{ma_npp}", response_model=schemas.DistributorResponse)
def edit_distributor(ma_npp: str, distributor: schemas.DistributorEditRequest, db: Session = Depends(get_db)):
    db_distributor = get_distributor_by_ma_npp(ma_npp, db)
    data = distributor.model_dump(exclude_none=True)

    # Check if there are any changes
    if not any(getattr(db_distributor, k) != v for k, v in data.items()):
        raise HTTPException(status_code=304, detail="No modifications")

    # Encrypt fields if present in data
    if data.get("dc_npp"):
        data["dc_npp"] = call_function_services.encrypt_des(data["dc_npp"], key_des)
    if data.get("sdt_npp"):
        data["sdt_npp"] = call_function_services.encrypt_caesar(data["sdt_npp"], key)
    if data.get("email_npp"):
        data["email_npp"] = call_function_services.encrypt_rsa(data["email_npp"], public_key_rsa)

    # Update fields in db_distributor
    for k, v in data.items():
        setattr(db_distributor, k, v)

    db.commit()
    db.refresh(db_distributor)
    return db_distributor

@router.delete("/delete/{ma_npp}", response_model=dict)
def delete_distributor(ma_npp: str, db: Session = Depends(get_db)):
    db_distributor = get_distributor_by_ma_npp(ma_npp, db)
    db.delete(db_distributor)
    db.commit()
    return {"detail": "Distributor deleted successfully"}
