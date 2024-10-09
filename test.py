# Hàm tính modulo ngược của key
def mod_inverse(key: int, m: int) -> int:
    for i in range(1, m):
        if (key * i) % m == 1:
            return i
    raise ValueError(f"Modular inverse for key {key} does not exist with mod {m}.")

# Hàm mã hóa Caesar phép nhân
def encrypt_multiplicative_caesar(plaintext: str, key: int) -> str:
    result = ""
    for char in plaintext:
        # Lấy mã ASCII của ký tự
        char_code = ord(char)
        # Mã hóa theo phép nhân với modulo 256 (tất cả ký tự ASCII)
        encrypted_char_code = (char_code * key) % 256
        result += chr(encrypted_char_code)
    return result

# Hàm giải mã Caesar phép nhân
def decrypt_multiplicative_caesar(ciphertext: str, key: int) -> str:
    result = ""
    mod_inv = mod_inverse(key, 256)  # Tính toán modulo ngược của key với 256
    for char in ciphertext:
        # Lấy mã ASCII của ký tự
        char_code = ord(char)
        # Giải mã theo phép nhân modulo ngược với 256
        decrypted_char_code = (char_code * mod_inv) % 256
        result += chr(decrypted_char_code)
    return result


plaintext = "HELlo @!#$% 123"
key = 3

# Mã hóa
ciphertext = encrypt_multiplicative_caesar(plaintext, key)
print("Ciphertext:", ciphertext,"|")

# Giải mã
decrypted_text = decrypt_multiplicative_caesar(ciphertext, key)
print("Decrypted:", decrypted_text, "|")
