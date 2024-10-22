from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from utils.callfunction import *
from module.v1.Users import schemas, models, services
from module.v1.Users.config import *
from db.config import *

router = APIRouter(
    prefix="/mudule/v1/users",
    tags=["users"],
)

@router.get("/all", response_model=list[schemas.UserResponse])
def get_all_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users no exist")
    return users

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    ma_kh = services.generate_ma_kh()
    db_user = db.query(models.User).filter(models.User.ma_kh == ma_kh).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    encrypt_email=encrypt_caesar(user.email_kh, key)
    services.validate_email_format(user.email_kh)
    db_user = services.check_existing_email(db, encrypt_email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    services.check_password_length(user.pass_kh)
    encrypt_pass = services.encrypt_multiplicative_caesar(user.pass_kh, key)
    #DES
    encrypt_des_name = encrypt_des(user.ten_kh, key_des)

    db_user = models.User(
        ma_kh=ma_kh,
        pass_kh= encrypt_pass,
        ten_kh=encrypt_des_name,
        sdt_kh=user.sdt_kh,
        email_kh=encrypt_email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", status_code=201,responses={
                201: {"description": "Login user success"},
                })
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    en_email =encrypt_caesar( user.email_kh, key)
    db_user = db.query(models.User).filter(models.User.email_kh == en_email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Invalid username or password")
    services.check_password_length(user.pass_kh)
    en_pass = services.encrypt_multiplicative_caesar(user.pass_kh, key)
    if not services.verify_password(en_pass, db_user.pass_kh):
        raise HTTPException(status_code=401, detail="Password is incorrect!")
    
    return {"message": "Login successful"}

@router.put("/edit/{ma_kh}", response_model=schemas.UserResponse)
def edit_user(ma_kh: str, user: schemas.UserEditResquest, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.ma_kh == ma_kh).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    data = user.model_dump(exclude_none=True)
    if not any(getattr(db_user, k) != value for k, value in data.items()):
        raise HTTPException(status_code=304, detail="No modifications")
    
    if data.get("pass_kh"):
        encrypt_password  = encrypt_caesar(data["pass_kh"], key)
        data["pass_kh"] = encrypt_password
    #DES
    if data.get("ten_kh"):
        encrypt_name = encrypt_des(data["ten_kh"], key)
        data["ten_kh"] = encrypt_name
    if data.get("sdt_kh"):
        encrypt_phone=encrypt_caesar(data["sdt_kh"], key)
        data["sdt_kh"] = encrypt_phone

    for k, value in data.items():
        setattr(db_user, k, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/delete/{ma_kh}", response_model=dict)
def delete_user(ma_kh: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.ma_kh == ma_kh).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    
    return {"detail": "User deleted successfully"}