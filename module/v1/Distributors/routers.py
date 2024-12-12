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
        raise HTTPException(status_code=404, detail="Nhà phân phối với mã {ma_npp} không tìm thấy!")
    return db_distributor

@router.get("/all", response_model=list[schemas.DistributorResponse])
def get_all_distributors(db: Session = Depends(get_db)):
    distributors = db.query(models.Distributor).all()
    
    if not distributors:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhà phân phối nào")
    
    # Chuẩn bị dữ liệu đã giải mã
    result = [
        schemas.DistributorResponse(
            ma_npp=distributor.ma_npp,
            ten_npp=distributor.ten_npp,
            email_npp=call_function_services.decrypt_rsa(distributor.email_npp, private_key_rsa),
            sdt_npp=call_function_services.decrypt_lai(distributor.sdt_npp, private_key_rsa),
            dc_npp=distributor.dc_npp,
        )
        for distributor in distributors
    ]
    
    
    return result

@router.get("/detail", response_model=schemas.DistributorResponse)
async def get_detail_distributor(ma_npp: str, db: Session = Depends(get_db)):
    data_distributor = get_distributor_by_ma_npp(ma_npp, db)
    return data_distributor

@router.post("/register", response_model=schemas.DistributorResponse, status_code=200)
def create_distributor(distributor: schemas.DistributorRegister, db: Session = Depends(get_db)):
    # Generate unique `ma_npp`
    ma_npp = services.generate_ma_npp()
    if db.query(models.Distributor).filter(models.Distributor.ma_npp == ma_npp).first():
        raise HTTPException(status_code=400, detail="Nhà phân phối đã tồn tại")

    # Validate and encrypt email
    services.validate_email_format(distributor.email_npp)
    encrypt_email = call_function_services.encrypt_rsa(distributor.email_npp, public_key_rsa)
    if services.check_existing_email(db, encrypt_email):
        raise HTTPException(status_code=400, detail="Email nhà phân phối đã tồn tại")

    # Encrypt other fields
    encrypt_location = call_function_services.encrypt_des(distributor.dc_npp, key_des)
    encrypt_phone = call_function_services.encrypt_lai(distributor.sdt_npp, public_key_rsa, key_des)

    # Create new distributor entry
    db_distributor = models.Distributor(
        ma_npp=ma_npp,
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
    return {"detail": "Xóa nhà phân phối thành công"}
