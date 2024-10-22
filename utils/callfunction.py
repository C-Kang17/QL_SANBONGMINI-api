from fastapi import APIRouter, HTTPException, Depends
from db.config import *
import cx_Oracle

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
