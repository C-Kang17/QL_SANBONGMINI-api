from fastapi import FastAPI
# from db.database import get_db,create_default_admin
from fastapi.middleware.cors import CORSMiddleware
from module.v1.Users.routers import router as user_router
from module.v1.Staffs.routers import router as staff_router
from module.v1.Distributors.routers import router as distributor_router
from module.v1.Order.routers import router as Order_router
from module.v1.Order_items.routers import router as Orderitem_router
from module.v1.Loaisan.routers import router as Loaisan_router
from module.v1.San.routers import router as San_router
import uvicorn
app = FastAPI()


# @app.on_event("startup")
# def startup_event():
#     db = next(get_db())  # Tạo session để kết nối đến DB
#     create_default_admin(db)  # Gọi hàm tạo tài khoản admin

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các domain
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP (GET, POST, PUT, DELETE, ...)
    allow_headers=["*"],  # Cho phép tất cả các headers
)

app.include_router(user_router, prefix="/users")
app.include_router(staff_router, prefix="/staffs")
app.include_router(distributor_router, prefix="/distributors")
app.include_router(Order_router, prefix="/orders")
app.include_router(Orderitem_router, prefix="/order-items")
app.include_router(Loaisan_router, prefix="/loaisan")
app.include_router(San_router, prefix="/san")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
