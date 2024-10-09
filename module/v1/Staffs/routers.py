from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.config import DB_HOST
from module.v1.Staffs import schemas, models, services
from config import *
import cx_Oracle
router = APIRouter(
    prefix="/mudule/v1/staffs",
    tags=["staffs"],
)
def encrypt_caesar(p: str, k: int) -> str:
    try:
        # Thiết lập kết nối với Oracle
        dsn = cx_Oracle.makedsn(DB_HOST, 1521, service_name="orcl2")
        connection = cx_Oracle.connect(user="QL_SANBONGMINI", password="123", dsn=dsn)
        cursor = connection.cursor()

        # Gọi hàm ENCRYPT_CAESAR từ Oracle
        encrypted= cursor.callfunc("encryptExtCaesarMult", cx_Oracle.STRING, [p, k])

        cursor.close()
        connection.close()
        return encrypted
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

def decrypt_caesar(enc: str, k: int) -> str:
    try:
        # Thiết lập kết nối với Oracle
        dsn = cx_Oracle.makedsn(DB_HOST, 1521, service_name="orcl2")
        connection = cx_Oracle.connect(user="QL_SANBONGMINI", password="123", dsn=dsn)
        cursor = connection.cursor()

        # Gọi hàm ENCRYPT_CAESAR từ Oracle
        encrypted= cursor.callfunc("decryptExtCaesarMult", cx_Oracle.STRING, [enc, k])

        cursor.close()
        connection.close()
        return encrypted
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

# Đăng ký người dùng mới
@router.post("/register/", response_model=schemas.StaffRegisterResponse)
def register_staff(staff: schemas.StaffRegister, db: Session = Depends(get_db)):
    ma_nv = services.generate_ma_nv()
    # Kiểm tra người dùng đã tồn tại chưa
    db_staff = db.query(models.Staff).filter(models.Staff.ma_nv == ma_nv).first()
    if db_staff:
        raise HTTPException(status_code=400, detail="Staff already registered")
    

    encrypt_email=encrypt_caesar(staff.email_nv, key)
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
        email_nv= encrypt_email,
        chuc_vu= staff.chuc_vu.lower()
    )
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

# Đăng nhập người dùng
@router.post("/login/", status_code=200,responses={
                200: {"model": schemas.StaffLoginResponse,"description": "Login staff success"},
                })
def login(staff: schemas.StaffLogin, db: Session = Depends(get_db)):
    encrypt_email=encrypt_caesar(staff.email_nv, key)
    db_staff = db.query(models.Staff).filter(models.Staff.email_nv == encrypt_email).first()

    if db_staff is None:
        raise HTTPException(status_code=404, detail="Invalid email or password")
    
    en_pass = services.encrypt_multiplicative_caesar(staff.pass_nv, key)

    #Kiểm tra mật khẩu có chính xác không
    if not services.verify_password(en_pass, db_staff.pass_nv):
        raise HTTPException(status_code=401, detail="Password is incorrect!")
    responses = schemas.StaffLoginResponse(
        chuc_vu = db_staff.chuc_vu
    )

    return responses