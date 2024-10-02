from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from module.v1.Staffs import schemas, models, services

router = APIRouter(
    prefix="/mudule/v1/staffs",
    tags=["staffs"],
)

# Đăng ký người dùng mới
@router.post("/register/", response_model=schemas.StaffRegisterResponse)
def register_staff(staff: schemas.StaffRegister, db: Session = Depends(get_db)):
    ma_nv = services.generate_ma_nv()
    # Kiểm tra người dùng đã tồn tại chưa
    db_staff = db.query(models.Staff).filter(models.Staff.ma_nv == ma_nv).first()
    if db_staff:
        raise HTTPException(status_code=400, detail="Staff already registered")
    
    # Kiểm tra email của người dùng đã tồn tại chưa
    services.validate_email_format(staff.email_nv)
    db_staff = services.check_existing_email(db, staff.email_nv)
    if db_staff:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Kiểm tra độ dài mật khẩu
    services.check_password_length(staff.pass_nv)
    
    # Tạo người dùng mới
    db_staff = models.Staff(
        ma_nv=ma_nv,
        ten_nv= staff.ten_nv,
        pass_nv= staff.pass_nv,
        sdt_nv= staff.sdt_nv,
        dia_chi= staff.dia_chi,
        email_nv= staff.email_nv,
        chuc_vu= staff.chuc_vu
    )
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

# Đăng nhập người dùng
@router.post("/login/", status_code=201,responses={
                201: {"description": "Login staff success"},
                })
def login(staff: schemas.StaffLogin, db: Session = Depends(get_db)):
    db_staff = db.query(models.Staff).filter(models.Staff.email_nv == staff.email_nv).first()

    if db_staff is None:
        raise HTTPException(status_code=404, detail="Invalid email or password")
    
    # Kiểm tra độ dài mật khẩu
    services.check_password_length(staff.pass_nv)

    #Kiểm tra mật khẩu có chính xác không
    if not services.verify_password(staff.pass_nv, db_staff.pass_nv):
        raise HTTPException(status_code=401, detail="Password is incorrect!")
    
    return {"message": "Login successful"}