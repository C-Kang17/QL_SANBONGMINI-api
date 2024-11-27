from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from utils import callfunction as call_function_services
from module.v1.Staffs import schemas, models, services
from db.config import *

router = APIRouter(
    prefix="/module/v1/staffs",
    tags=["staffs"],
)


def get_staff_by_ma_nv(ma_nv: str, db: Session):
    db_staff = db.query(models.Staff).filter(models.Staff.ma_nv == ma_nv).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Nhân viên với mã {ma_nv} không tìm thấy")
    return db_staff

@router.get("/all", response_model=list[schemas.StaffResponse])
def get_all_staff(db: Session = Depends(get_db)):
    staffs = db.query(models.Staff).all()
    if not staffs:
        raise HTTPException(status_code=404, detail="không tìm thấy nhân viên nào")
    result = [
        schemas.StaffResponse(
            ma_nv=staff.ma_nv,
            ten_nv=staff.ten_nv,
            email_nv=call_function_services.decrypt_rsa(staff.email_nv, private_key_rsa),
            sdt_nv=staff.sdt_nv,
            dia_chi=staff.dia_chi,
            chuc_vu=staff.chuc_vu,
        )
        for staff in staffs
    ]
    
    return result

@router.get("detail", response_model=schemas.StaffResponse)
def get_detail_users(ma_nv: str, db: Session = Depends(get_db)):
    staff = get_staff_by_ma_nv(ma_nv, db)
    if not staff:
        raise HTTPException(status_code=404, detail="Nhân viên với mã {ma_nv} không tìm thấy!")
    result = [
        schemas.StaffResponse(
            ma_nv=staff.ma_nv,
            ten_nv=staff.ten_nv,
            email_nv=call_function_services.decrypt_rsa(staff.email_nv, private_key_rsa),
            sdt_nv=staff.sdt_nv,
            dia_chi=staff.dia_chi,
            chuc_vu=staff.chuc_vu,
        )
    ]
    
    return result

@router.post("/register", response_model=schemas.StaffResponse, status_code=200)
def register_staff(staff: schemas.StaffRegister, db: Session = Depends(get_db)):
    ma_nv = services.generate_ma_nv()
    if db.query(models.Staff).filter(models.Staff.ma_nv == ma_nv).first():
        raise HTTPException(status_code=400, detail="Nhân viên đã đăng ký rồi")

    # Validate and encrypt email
    services.validate_email_format(staff.email_nv)
    encrypt_email = call_function_services.encrypt_rsa(staff.email_nv, public_key_rsa)
    if services.check_existing_email(db, encrypt_email):
        raise HTTPException(status_code=400, detail="Email đã tồn tại rồi !")

    # Validate and encrypt password
    services.check_password_length(staff.pass_nv)
    encrypt_pass = call_function_services.encrypt_lai(staff.pass_nv, public_key_rsa, key_des)

    # Encrypt address
    encrypt_des_address = call_function_services.encrypt_des(staff.dia_chi, key_des)

    # Create new staff entry
    db_staff = models.Staff(
        ma_nv=ma_nv,
        ten_nv=staff.ten_nv,
        pass_nv=encrypt_pass,
        sdt_nv=staff.sdt_nv,
        dia_chi=encrypt_des_address,
        email_nv=encrypt_email,
        chuc_vu=staff.chuc_vu.lower()
    )
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

@router.post("/login", response_model=schemas.StaffLoginResponse, status_code=200)
def login(staff: schemas.StaffLogin, db: Session = Depends(get_db)):
    db_staff = db.query(models.Staff).filter(models.Staff.ma_nv == staff.ma_nv).first()
    if not db_staff:
        raise HTTPException(status_code=404, detail="Mã nhân viên hoặc password không chính xác")

    en_pass = call_function_services.encrypt_lai(staff.pass_nv, public_key_rsa, key_des)
    if not services.verify_password(en_pass, db_staff.pass_nv):
        raise HTTPException(status_code=401, detail="Password không đúng!")

    return schemas.StaffLoginResponse(ma_nv=db_staff.ma_nv,ten_nv=db_staff.ten_nv,chuc_vu=db_staff.chuc_vu)

@router.put("/edit/{ma_nv}", response_model=schemas.StaffResponse)
def edit_staff(ma_nv: str, staff: schemas.StaffEditRequest, db: Session = Depends(get_db)):
    db_staff = get_staff_by_ma_nv(ma_nv, db)
    data = staff.model_dump(exclude_none=True)

    # Check if there are any changes
    if not any(getattr(db_staff, k) != v for k, v in data.items()):
        raise HTTPException(status_code=304, detail="No modifications")

    # Encrypt fields if present in data
    if data.get("pass_nv"):
        data["pass_nv"] = call_function_services.encrypt_lai(data["pass_nv"], public_key_rsa, key_des)
    if data.get("email_nv"):
        data["email_nv"] = call_function_services.encrypt_rsa(data["email_nv"], public_key_rsa)
    if data.get("dia_chi"):
        data["dia_chi"] = call_function_services.encrypt_des(data["dia_chi"], key_des)

    # Update fields in db_staff
    for k, v in data.items():
        setattr(db_staff, k, v)

    db.commit()
    db.refresh(db_staff)
    return db_staff

@router.delete("/delete/{ma_nv}", response_model=dict)
def delete_staff(ma_nv: str, db: Session = Depends(get_db)):
    db_staff = get_staff_by_ma_nv(ma_nv, db)
    db.delete(db_staff)
    db.commit()
    return {"detail": "Xóa nhân viên thành công"}
