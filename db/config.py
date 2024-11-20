import re
import os

DB_HOST = os.getenv("DB_HOST", "localhost")  # Thay đổi IP khi cần thiết
DB_PORT = "1521"
DB_USER = "QL_SANBONGMINI"
DB_PASS = "123"
DB_SID = "orcl2"

key = 7
key_des = "Thats my Kung Fu"

public_key_rsa = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCamo3V09odclfSlMe25GowZ/TqdSy7cTlMjFndxPVcGgOUt7l5nUQREEOkkFLYfyejOqTRNiRN0rSZ5W0m5RRWrLfa1WVMGxmnZr5nlHz46GdbEdt69URJOPoZiPpueWrG45WTGIWP6Ka3Fok7DpdXJVGytGcGFsTN5D0XmAbMpQIDAQAB"
private_key_rsa = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAJqajdXT2h1yV9KUx7bkajBn9Op1LLtxOUyMWd3E9VwaA5S3uXmdRBEQQ6SQUth/J6M6pNE2JE3StJnlbSblFFast9rVZUwbGadmvmeUfPjoZ1sR23r1REk4+hmI+m55asbjlZMYhY/oprcWiTsOl1clUbK0ZwYWxM3kPReYBsylAgMBAAECgYEAj7Krtl2M0+XdfxtObc3sbUWSvQFgLHDWozGorZpNu+dqAKarvD/SblHBrYl/lz7IpszxOIusPrFjr88xHv+5YEyexof1yKxdMW9wtBCSnkoAZZC8ni6ypK9h5Q0V3YwZiLpSC8i/58pTT042YNL4eCsDqPWQzBmtoHWDNtH6uRkCQQDIiam2IuJVHzVXcxnrMX1t1aZI9HUr4WLAsxeLfCprWn/WAVlY7Y/X34fhzYBX2mPmqlMWuN/FCQs/RclRzkWXAkEAxVyzsfsbwTrZBZxVHIdOvkMz3BDToHL3Iy4EWzvNcq/smIyCUyQ9hAKPmZKsbXSPGzN0ysi6hx3Zeg7yzYofIwJASe8HFNFzpHJnFiCnc6DBX5cfQVJvSIhGAkmE6rYSZZXt/5ZrvG+JUstkq4k6QimQH2C4VW4/gcM91EwEVxa3bQJAU7vR7XgpPWEXRF8gaRsrGGPws7Rb5R4BpmZWqNKFhtwG2G38uQOOKdzgSfrFtyaVtKevLH3fTYYnh7ah4vxv2wJAYC/8TV2AUfKj/7aZkVoilRJqKRIl5VLzU12aDzHq//WKXValT6P83wC6sg7UCAv1Zfpmww+jM2XN4mGw8VAy/Q=="




def extract_keys(keys_str: str) -> dict:
    # Biểu thức chính quy để tách public key và private key
    public_key = re.search(r"publicKey start\*+\s*(.*?)\s*\*+publicKey end", keys_str, re.DOTALL)
    private_key = re.search(r"privateKey start\*+\s*(.*?)\s*\*+privateKey end", keys_str, re.DOTALL)
    # Lấy giá trị public key và private key
    public_key_value = public_key.group(1).strip() if public_key else None
    private_key_value = private_key.group(1).strip() if private_key else None
    # Trả về dictionary chứa cả hai khóa
    return {
        "public_key": public_key_value,
        "private_key": private_key_value
    }

