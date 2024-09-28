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
