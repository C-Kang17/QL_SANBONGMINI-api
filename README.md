# Trước tiên thay đổi địa chỉ ip trong db/config và db/database
### Bước 1: bật CMD nhập
```bash
ipconfig
```
kết quả ra rất nhiều tìm mục Wifi xem IPv4 Address là gì copy lại.
### Bước 2: Tại db/config.py
Dựa vào các thông tin Oracle của bạn mà thay cho phù hợp
```bash
DB_HOST = os.getenv("DB_HOST", "localhost")  # Nhập DB_HOST như vậy không thay đổi
DB_PORT = "1521"
DB_USER = "QL_SANBONGMINI" # Giống username trong oralce bạn tạo
DB_PASS = "123"
DB_SID = "orcl"
```
// **như vậy là xong :))**   

# Để chạy trên docker
### Bước 1: Bật Docker desktop (Bạn đã cài, nếu chưa hãy cài)
### Bước 2: mở CMD của folder chứa dự án.
### Bước 3: nhập lệnh sau
```bash
bin\windows\start.bat
```
> #### Tip!!!: Khi bạn ấn chữ b đầu tiên bạn ấn tab trên bàn phím là nó sẽ tự động điền cho bạn, xong rồi \ ấn w rồi ấn tab là nó sẽ điền cho mình cứ thế \ cuối cùng ấn b ấn tab sẽ điền ra cho bạn !!!

### Vậy là xong docker!!!
<!-- docker network create doan_network
docker run --network doan_network -p 8000:8000 doan-api   -->
<!-- ```bash
# Kết nối trong trường.
docker run --network=host doan-api
``` -->
*tắt chương trình*
```bash
Ctrl + C
```

# Để chạy tại localhost
### Bước 1: mở CMD của folder chứa dự án.
### Bước 2: nhập lệnh sai
```bash
uvicorn main:app --reload
```
hoặc là 
```bash
bin\windows\test.bat
```
#### Tip: như bên trên docker bạn chỉ cần ấn chữ cái đầu và ấn phím TAB trên bàn phím
*tắt chương trình*
```bash
Ctrl + C
```
