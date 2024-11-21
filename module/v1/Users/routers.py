from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from utils import callfunction as call_function_services
from module.v1.Users import schemas, models, services
from db.config import *

router = APIRouter(
    prefix="/module/v1/users",
    tags=["users"],
)

def get_user_by_ma_kh(ma_kh: str, db: Session):
    db_user = db.query(models.User).filter(models.User.ma_kh == ma_kh).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/all", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    result = [
        schemas.UserResponse(
            ma_kh=user.ma_kh,
            ten_kh=user.ten_kh,
            email_kh=call_function_services.decrypt_rsa(user.email_kh, private_key_rsa),
            sdt_kh=user.sdt_kh,
        )
        for user in users
    ]
    
    return result

@router.post("/register", response_model=schemas.UserResponse, status_code=200)
def register_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    ma_kh = services.generate_ma_kh()
    if db.query(models.User).filter(models.User.ma_kh == ma_kh).first():
        raise HTTPException(status_code=400, detail="User already registered")

    # Validate and encrypt email
    services.validate_email_format(user.email_kh)
    encrypt_email = call_function_services.encrypt_rsa(user.email_kh, public_key_rsa)
    if services.check_existing_email(db, encrypt_email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate and encrypt password
    services.check_password_length(user.pass_kh)
    encrypt_pass = call_function_services.encrypt_lai(user.pass_kh, public_key_rsa, key_des)
    # encrypt_pass = call_function_services.encrypt_caesar(user.pass_kh, key)
    # Encrypt phone number
    encrypt_phone = call_function_services.encrypt_des(user.sdt_kh, key_des)

    # Create new user entry
    db_user = models.User(
        ma_kh=ma_kh,
        pass_kh=encrypt_pass,
        ten_kh=user.ten_kh,
        sdt_kh=encrypt_phone,
        email_kh=encrypt_email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



@router.post("/login", response_model=schemas.UserLoginResponse, status_code=201)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    en_email = call_function_services.encrypt_rsa(user.email_kh, public_key_rsa)
    db_user = db.query(models.User).filter(models.User.email_kh == en_email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Invalid username or password")

    # Validate and check password
    services.check_password_length(user.pass_kh)
    en_pass = call_function_services.encrypt_lai(user.pass_kh, public_key_rsa, key_des)
    if not services.verify_password(en_pass, db_user.pass_kh):
        raise HTTPException(status_code=401, detail="Incorrect password")

    decrypt_email = call_function_services.decrypt_rsa(db_user.email_kh, private_key_rsa)
    response = {
        "ma_kh": db_user.ma_kh,
        "ten_kh": db_user.ten_kh,
        "email_kh": decrypt_email,
        "sdt_kh": db_user.sdt_kh 
    }
    print(response)
    return response

@router.put("/edit/{ma_kh}", response_model=schemas.UserResponse)
def edit_user(ma_kh: str, user: schemas.UserEditRequest, db: Session = Depends(get_db)):
    db_user = get_user_by_ma_kh(ma_kh, db)
    data = user.model_dump(exclude_none=True)

    # Encrypt and update fields if changed
    if data.get("pass_kh"):
        data["pass_kh"] = call_function_services.encrypt_lai(data["pass_kh"], public_key_rsa, key_des)
    if data.get("sdt_kh"):
        data["sdt_kh"] = call_function_services.encrypt_des(data["sdt_kh"], key_des)

    # Update only if there are changes
    if not any(getattr(db_user, k) != v for k, v in data.items()):
        raise HTTPException(status_code=304, detail="No modifications")

    for key_chk, value in data.items():
        setattr(db_user, key_chk, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/delete/{ma_kh}", response_model=dict)
def delete_user(ma_kh: str, db: Session = Depends(get_db)):
    db_user = get_user_by_ma_kh(ma_kh, db)
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}
