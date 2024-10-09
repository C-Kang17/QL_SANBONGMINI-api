from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from module.v1.Users import schemas, models, services
from db.config import DB_HOST
from config import *
import cx_Oracle

router = APIRouter(
    prefix="/mudule/v1/users",
    tags=["users"],
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
@router.post("/register/", response_model=schemas.UserRegisterResponse)
def register_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    ma_kh = services.generate_ma_kh()

    # Kiểm tra người dùng đã tồn tại chưa
    db_user = db.query(models.User).filter(models.User.ma_kh == ma_kh).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    encrypt_email=encrypt_caesar(user.email_kh, key)
    # Kiểm tra email của người dùng đã tồn tại chưa
    services.validate_email_format(user.email_kh)

    db_user = services.check_existing_email(db, encrypt_email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Kiểm tra độ dài mật khẩu
    services.check_password_length(user.pass_kh)
    encrypt_pass = services.encrypt_multiplicative_caesar(user.pass_kh, key)

    # Tạo người dùng mới
    db_user = models.User(
        ma_kh=ma_kh,
        pass_kh= encrypt_pass,
        ten_kh=user.ten_kh,
        sdt_kh=user.sdt_kh,
        email_kh=encrypt_email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Đăng nhập người dùng
@router.post("/login/", status_code=201,responses={
                201: {"description": "Login user success"},
                })
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    en_email =encrypt_caesar( user.email_kh, key)
    db_user = db.query(models.User).filter(models.User.email_kh == en_email).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Invalid username or password")
    
    # Kiểm tra độ dài mật khẩu
    services.check_password_length(user.pass_kh)
    en_pass = services.encrypt_multiplicative_caesar(user.pass_kh, key)

    #Kiểm tra mật khẩu có chính xác không
    if not services.verify_password(en_pass, db_user.pass_kh):
        raise HTTPException(status_code=401, detail="Password is incorrect!")
    
    return {"message": "Login successful"}