from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from utils.callfunction import *
from module.v1.Staffs import schemas, models, services
from module.v1.Staffs.config import *
from db.config import *

router = APIRouter(
    prefix="/mudule/v1/staffs",
    tags=["staffs"],
)

@router.get("/all", response_model=list[schemas.StaffResponse])
def get_all_staff(db: Session = Depends(get_db)):
    staffs = db.query(models.Staff).all()
    if not staffs:
        raise HTTPException(status_code=404, detail="No staff found")
    return staffs

@router.post("/register", response_model=schemas.StaffResponse)
def register_staff(staff: schemas.StaffRegister, db: Session = Depends(get_db)):
    ma_nv = services.generate_ma_nv()
    db_staff = db.query(models.Staff).filter(models.Staff.ma_nv == ma_nv).first()
    if db_staff:
        raise HTTPException(status_code=400, detail="Staff already registered")
    encrypt_email=encrypt_caesar(staff.email_nv, key)
    services.validate_email_format(staff.email_nv)
    db_staff = services.check_existing_email(db, staff.email_nv)
    if db_staff:
        raise HTTPException(status_code=400, detail="Email already registered")
    services.check_password_length(staff.pass_nv)
    encrypt_pass = services.encrypt_multiplicative_caesar(staff.pass_nv, key)

    #DES address
    encrypt_des_address = encrypt_des(staff.dia_chi,key_des)
    db_staff = models.Staff(
        ma_nv=ma_nv,
        ten_nv= staff.ten_nv,
        pass_nv= encrypt_pass,
        sdt_nv= staff.sdt_nv,
        dia_chi= encrypt_des_address,
        email_nv= encrypt_email,
        chuc_vu= staff.chuc_vu.lower()
    )
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff


@router.post("/login", status_code=200,responses={
                200: {"model": schemas.StaffLoginResponse,"description": "Login staff success"},
                })
def login(staff: schemas.StaffLogin, db: Session = Depends(get_db)):
    db_staff = db.query(models.Staff).filter(models.Staff.ma_nv == staff.ma_nv).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Invalid 'Mã Nhân viên' or password")
    en_pass = services.encrypt_multiplicative_caesar(staff.pass_nv, key)
    if not services.verify_password(en_pass, db_staff.pass_nv):
        raise HTTPException(status_code=401, detail="Password is incorrect!")
    responses = schemas.StaffLoginResponse(
        chuc_vu = db_staff.chuc_vu
    )
    return responses

@router.put("/edit/{ma_nv}", response_model=schemas.StaffResponse)
def edit_staff(ma_nv: str, staff: schemas.StaffEditRequest, db: Session = Depends(get_db)):
    db_staff = db.query(models.Staff).filter(models.Staff.ma_nv == ma_nv).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")

    data = staff.model_dump(exclude_none=True)

    if not any(getattr(db_staff, k) != value for k, value in data.items()):
        raise HTTPException(status_code=304, detail="No modifications")
    
    if data.get("pass_nv"):
        en_pass = services.encrypt_multiplicative_caesar(data["pass_nv"], key)
        data["pass_nv"] = en_pass
    if data.get("email_nv"):
        encrypt_email=encrypt_caesar(data["email_nv"], key)
        data["email_nv"] = encrypt_email
    if data.get("dia_chi"):
        encrypt_address = encrypt_des(staff.dia_chi,key_des)
        data["dia_chi"] = encrypt_address

    for k, value in data.items():
        setattr(db_staff, k, value)

    db.commit()
    db.refresh(db_staff)
    return db_staff

@router.delete("/delete/{ma_nv}", response_model=dict)
def delete_staff(ma_nv: str, db: Session = Depends(get_db)):
    db_staff = db.query(models.Staff).filter(models.Staff.ma_nv == ma_nv).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")

    db.delete(db_staff)
    db.commit()
    
    return {"detail": "Staff deleted successfully"}