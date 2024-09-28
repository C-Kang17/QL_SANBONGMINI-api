# Trước tiên thay đổi địa chỉ ip trong db/config và db/database
### Bước 1: bật CMD nhập
```bash
ipconfig
```
kết quả ra rất nhiều tìm mục Wifi xem IPv4 Address là gì copy lại.   
vào db/config và db/database parst cái ip đó thế cái ip được hiện bên trong
> #### Tại db/config.py
Thay thế IP trong biến DB_HOST
> #### Tại db/database.py
Thay thế IP trong đây 
```bash
DB_HOST = os.getenv("DB_HOST", "192.168.1.6")
```
// **như vậy là xong :))**   

# Để chạy trên docker
### Bước 1: mở CMD của folder chứa dự án.
### Bước 2: nhập lệnh sau
```bash
docker build -t doan-api . 
```
### Bước 3: sau khi đã build xong ta sẽ chạy lệnh run

```bash
docker run -p 8000:8000 doan-api
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
