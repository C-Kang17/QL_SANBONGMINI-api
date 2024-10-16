from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from module.v1.Staffs import schemas, models, services
from module.v1.Staffs.config import *
from db.config import *
import cx_Oracle
router = APIRouter(
    prefix="/mudule/v1/staffs",
    tags=["staffs"],
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

#Lấy tất cả thông tin của staffs
@router.get("/all", response_model=list[schemas.StaffResponse])
def get_all_staff(db: Session = Depends(get_db)):
    staffs = db.query(models.Staff).all()
    if not staffs:
        raise HTTPException(status_code=404, detail="No staff found")
    return staffs

# Đăng ký người dùng mới
@router.post("/register", response_model=schemas.StaffResponse)
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
    en_pass = services.encrypt_multiplicative_caesar(staff.pass_nv, key)
    # Tạo người dùng mới
    db_staff = models.Staff(
        ma_nv=ma_nv,
        ten_nv= staff.ten_nv,
        pass_nv= en_pass,
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
@router.post("/login", status_code=200,responses={
                200: {"model": schemas.StaffLoginResponse,"description": "Login staff success"},
                })
def login(staff: schemas.StaffLogin, db: Session = Depends(get_db)):
    db_staff = db.query(models.Staff).filter(models.Staff.ma_nv == staff.ma_nv).first()

    if db_staff is None:
        raise HTTPException(status_code=404, detail="Invalid 'Mã Nhân viên' or password")
    
    en_pass = services.encrypt_multiplicative_caesar(staff.pass_nv, key)

    #Kiểm tra mật khẩu có chính xác không
    if not services.verify_password(en_pass, db_staff.pass_nv):
        raise HTTPException(status_code=401, detail="Password is incorrect!")
    
    responses = schemas.StaffLoginResponse(
        chuc_vu = db_staff.chuc_vu
    )

    return responses

print(key)

@router.put("/edit/{ma_nv}", response_model=schemas.StaffResponse)
def edit_staff(ma_nv: str, staff: schemas.StaffEditRequest, db: Session = Depends(get_db)):
    # Lấy thông tin nhân viên từ database
    db_staff = db.query(models.Staff).filter(models.Staff.ma_nv == ma_nv).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")

    # Lấy dữ liệu hiện tại của staff từ database, sử dụng model_dump để loại bỏ các field None
    data = staff.model_dump(exclude_none=True)

    # Kiểm tra nếu không có thay đổi gì
    if not any(getattr(db_staff, k) != value for k, value in data.items()):
        raise HTTPException(status_code=304, detail="No modifications")
    
    if data.get("pass_nv"):
        en_pass = services.encrypt_multiplicative_caesar(data["pass_nv"], key)
        data["pass_nv"] = en_pass
    if data.get("email_nv"):
        encrypt_email=encrypt_caesar(data["email_nv"], key)
        data["email_nv"] = encrypt_email

    # Cập nhật các trường có thay đổi
    for k, value in data.items():
        setattr(db_staff, k, value)

    db.commit()
    db.refresh(db_staff)
    return db_staff