from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from module.v1 import schemas, models
router = APIRouter(
    prefix="/mudule/v1/users",
    tags=["users"],
)

# Đăng ký người dùng mới
@router.post("/register/", response_model=schemas.UserRegisterResponse)
def register_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    # Kiểm tra người dùng đã tồn tại chưa
    db_user = db.query(models.User).filter(models.User.ma_kh == user.ma_kh).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    # Kiểm tra email của người dùng đã tồn tại chưa
    db_user = db.query(models.User).filter(models.User.email_kh == user.email_kh).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    # Tạo người dùng mới
    db_user = models.User(
        ma_kh=user.ma_kh,
        pass_kh= user.pass_kh,
        ten_kh=user.ten_kh,
        sdt_kh=user.sdt_kh,
        email_kh=user.email_kh
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
    db_user = db.query(models.User).filter(models.User.email_kh == user.email_kh).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Invalid username or password")
    
    if db_user.pass_kh != user.pass_kh:
        raise HTTPException(status_code=401, detail="Password is incorrect!")
    
    return {"message": "Login successful"}