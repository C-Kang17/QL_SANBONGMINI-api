from fastapi import HTTPException
from db.config import *
import cx_Oracle
from sqlalchemy.orm import Session
# Caesar
def encrypt_caesar(p: str, k: int) -> str:
    try:
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        connection = cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn)
        cursor = connection.cursor()

        encrypted= cursor.callfunc("encryptExtCaesarMult", cx_Oracle.STRING, [p, k])

        cursor.close()
        connection.close()
        return encrypted
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

def decrypt_caesar(enc: str, k: int) -> str:
    try:
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        connection = cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn)
        cursor = connection.cursor()

        encrypted= cursor.callfunc("decryptExtCaesarMult", cx_Oracle.STRING, [enc, k])

        cursor.close()
        connection.close()
        return encrypted
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

# Des
def encrypt_des(plaintext: str, prikey: str) -> str:
    try:
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        connection = cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn)
        cursor = connection.cursor()

        encrypted_text = cursor.callfunc("DES.encrypt", cx_Oracle.STRING, [plaintext, prikey])

        cursor.close()
        connection.close()
        return encrypted_text
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
def decrypt_des(encrypted_text: str, prikey: str) -> str:
    try:
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        connection = cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn)
        cursor = connection.cursor()

        decrypted_text = cursor.callfunc("DES.decrypt", cx_Oracle.STRING, [encrypted_text, prikey])

        cursor.close()
        connection.close()
        return decrypted_text
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
# RSA
def encrypt_rsa(plaintext: str, publickey: str) -> str:
    try:
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        connection = cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn)
        cursor = connection.cursor()

        encrypted_text = cursor.callfunc("CRYPTO.RSA_ENCRYPT_NO_PADDING", cx_Oracle.STRING, [plaintext, publickey])

        cursor.close()
        connection.close()
        return encrypted_text
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
def decrypt_rsa(encrypted_text: str, privatekey: str) -> str:
    try:
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        connection = cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn)
        cursor = connection.cursor()

        decrypted_text = cursor.callfunc("CRYPTO.RSA_DECRYPT_NO_PADDING", cx_Oracle.STRING, [encrypted_text, privatekey])

        cursor.close()
        connection.close()
        return decrypted_text
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
# Lai
def encrypt_lai(plaintext: str, publickey: str, des_key: str) -> str:
    try:
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        connection = cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn)
        cursor = connection.cursor()
        encrypted_text = cursor.callfunc("HYBRID.ENCRYPT", cx_Oracle.STRING, [plaintext, publickey, des_key])

        cursor.close()
        connection.close()
        return encrypted_text
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
def decrypt_lai(encrypted_text: str, privatekey: str, des_key: str) -> str:
    try:
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        connection = cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn)
        cursor = connection.cursor()

        decrypted_text = cursor.callfunc("HYBRID.DECRYPT", cx_Oracle.STRING, [encrypted_text, des_key, privatekey])

        cursor.close()
        connection.close()
        return decrypted_text
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
#User
def create_user(username: str, password: str):
    """
    Call the pro_create_user procedure from the pkg_user package.
    """
    try:
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        with cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn) as connection:
            with connection.cursor() as cursor:
                cursor.callproc("pkg_user.pro_create_user", [username, password])
        return {"message": f"User {username} created successfully."}
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

def alter_user(username: str, password: str):
    """
    Call the pro_alter_user procedure from the pkg_user package.
    """
    try:
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        with cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn) as connection:
            with connection.cursor() as cursor:
                cursor.callproc("pkg_user.pro_alter_user", [username, password])
        return {"message": f"Password for user {username} updated successfully."}
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

def select_user(ma_kh: str):
    """
    Call the pro_select_user procedure from the pkg_user package.
    """
    try:
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        with cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn) as connection:
            with connection.cursor() as cursor:
                ref_cursor = connection.cursor()
                cursor.callproc("pkg_user.pro_select_user", [ma_kh, ref_cursor])

                # Fetch data from the ref cursor
                result = ref_cursor.fetchall()
                ref_cursor.close()

                # Convert result to dictionary
                return [
                    {
                        "MA_KH": row[0],
                        "TEN_KH": row[1],
                        "SDT_KH": row[2],
                        "EMAIL_KH": row[3],
                    }
                    for row in result
                ]
    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

def account_status(username: str) -> str:
    """
    Call the fun_account_status function to check account status.
    """
    try:
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        with cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn) as connection:
            with connection.cursor() as cursor:
                status = cursor.callfunc("fun_account_status", cx_Oracle.STRING, [username])
                print(f">>>>>>>>>>>>>>>>>>>>>> Status received: {status}")
        return status
    
    except cx_Oracle.DatabaseError as e:
        print(f"Error calling fun_account_status: {e}")
        raise HTTPException(status_code=500, detail="Error calling fun_account_status")


def connect_user(email_kh: str, pass_kh: str):
    try:
        # Gọi hàm fun_account_status để kiểm tra trạng thái tài khoản
        print(">>>>>>>>>>>>>>>>>>>>> email_kh no ngoac:  ",email_kh)
        status = account_status(email_kh)
        if status == "LOCKED(TIMED)":
            raise HTTPException(status_code=401, detail=f"Tài khoản {email_kh} đã bị khóa tạm thời 1 ngày.")
        elif status == "LOCKED":
            raise HTTPException(status_code=401, detail=f"Tài khoản {email_kh} đã bị khóa vĩnh viễn.")
        elif status == "EXPIRED":
            raise HTTPException(status_code=401, detail=f"Tài khoản {email_kh} đã hết hạn.")
        elif status != "OPEN":
            raise HTTPException(status_code=401, detail=f"Tài khoản {email_kh} không ở trạng thái OPEN!")
        email_kh_quoted = f'"{email_kh}"'
        print(">>>>>>>>>>>>>>>>>>>>> email_kh no ngoac:  ",email_kh_quoted)
        # Sử dụng email_kh và pass_kh để kết nối đến Oracle
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        try:
            connection = cx_Oracle.connect(user=email_kh_quoted, password=pass_kh, dsn=dsn)
            cursor = connection.cursor()
            cursor.close()
            connection.close()
            return {"message": f"Đăng nhập thành công với user {email_kh}."}
        except cx_Oracle.DatabaseError as e:
            if "ORA-01017: invalid username/password" in str(e):
                raise HTTPException(status_code=401, detail="Sai tên đăng nhập hoặc mật khẩu.")
            else:
                raise HTTPException(status_code=500, detail="Database error: " + str(e))

    except cx_Oracle.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
def pro_delete_user(username: str) -> bool:
    try:
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SID)
        with cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn) as connection:
            with connection.cursor() as cursor:
                email = decrypt_rsa(username, private_key_rsa)
                print(f">>>>>>>>>>>>>>>>>>>>>> user delete: {email}")
                cursor.callproc("pkg_user.pro_delete_user", [email])
                connection.commit()  # Commit the transaction
                return True

    except cx_Oracle.DatabaseError as e:
        print(f"Error deleting user: {e}")
        return False