from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from module.v1.Users.routers import router as user_router
from module.v1.Staffs.routers import router as staff_router
from module.v1.Distributors.routers import router as distributor_router
import uvicorn
app = FastAPI()

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
