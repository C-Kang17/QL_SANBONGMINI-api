from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from module.v1.Users import schemas, models, services
from module.v1.Users.config import key
from db.config import *
import cx_Oracle

router = APIRouter(
    prefix="/mudule/v1/users",
    tags=["users"],
)

def encrypt_caesar(p: str, k: int) -> str:
    try:
        # Thiết lập kết nối với Oracle
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        connection = cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn)
        cursor = connection.cursor()

        # Gọi hàm encryptExtCaesarMult từ Oracle
        encrypted= cursor.callfunc("encryptExtCaesarMult", cx_Oracle.STRING, [p, k])

        cursor.close()
        connection.close()
        return encrypted
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

def decrypt_caesar(enc: str, k: int) -> str:
    try:
        # Thiết lập kết nối với Oracle
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        connection = cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn)
        cursor = connection.cursor()

        # Gọi hàm decryptExtCaesarMult từ Oracle
        encrypted= cursor.callfunc("decryptExtCaesarMult", cx_Oracle.STRING, [enc, k])

        cursor.close()
        connection.close()
        return encrypted
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

#Lấy tất cả thông tin Users
@router.get("/all", response_model=list[schemas.UserResponse])
def get_all_user(db: Session = Depends(get_db)):
    staffs = db.query(models.User).all()
    if not staffs:
        raise HTTPException(status_code=404, detail="Users no exist")
    return staffs

# Đăng ký người dùng mới
@router.post("/register", response_model=schemas.UserResponse)
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
@router.post("/login", status_code=201,responses={
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

@router.put("/edit/{ma_kh}", response_model=schemas.UserResponse)
def edit_user(ma_kh: str, user: schemas.UserEditResquest, db: Session = Depends(get_db)):
    # Lấy thông tin người dùng từ database
    db_user = db.query(models.User).filter(models.User.ma_kh == ma_kh).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Lấy dữ liệu hiện tại của user từ database, sử dụng model_dump để loại bỏ các field None
    data = user.model_dump(exclude_none=True)

    # Kiểm tra nếu không có thay đổi gì
    if not any(getattr(db_user, k) != value for k, value in data.items()):
        raise HTTPException(status_code=304, detail="No modifications")
    
    if data.get("pass_kh"):
        encrypt_password  = encrypt_caesar(data["pass_kh"], key)
        data["pass_kh"] = encrypt_password
    if data.get("ten_kh"):
        encrypt_name = encrypt_caesar(data["ten_kh"], key)
        data["ten_kh"] = encrypt_name
    if data.get("sdt_kh"):
        encrypt_phone=encrypt_caesar(data["sdt_kh"], key)
        data["sdt_kh"] = encrypt_phone

    # Cập nhật các trường có thay đổi
    for k, value in data.items():
        setattr(db_user, k, value)

    db.commit()
    db.refresh(db_user)
    return db_user