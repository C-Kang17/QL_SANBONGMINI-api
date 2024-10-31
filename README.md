# Trước tiên thay đổi địa chỉ ip trong db/config và db/database
### Bước 1: bật CMD nhập
```bash
ipconfig
```
kết quả ra rất nhiều tìm mục Wifi xem IPv4 Address là gì copy lại.
### Bước 2: Tại db/config.py
Dựa vào các thông tin Oracle của bạn mà thay cho phù hợp
```bash
DB_HOST = "192.168.1.1"  # Thay đổi IP của bạn
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
bin\Windows\build.bat
```
> #### Tip!!!: Khi bạn ấn chữ b đầu tiên bạn ấn tab là nó sẽ tự động điền cho bạn, xong rồi \ ấn w rồi ấn tab là nó sẽ điền cho mình cứ thế \ cuối cùng ấn b ấn tab sẽ điền ra cho mình !!!
<!-- docker network create doan_network
docker run --network doan_network -p 8000:8000 doan-api   -->

### Bước 4: sau khi đã build xong ta sẽ chạy lệnh run
```bash
# Kết nối ngoài trường
bin\Windows\start.bat
```
```bash
# Kết nối trong trường.
docker run --network=host doan-api
```
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
*tắt chương trình*
```bash
Ctrl + C
```
