from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI()


products = [
    {
        "id": 1,
        "code": "SP001",
        "name": "Laptop Dell",
        "price": 15000000,
        "stock": 10
    },
    {
        "id": 2,
        "code": "SP002",
        "name": "Mouse Logitech",
        "price": 350000,
        "stock": 50
    }
]


# Model nhận dữ liệu tạo sản phẩm
class ProductCreate(BaseModel):
    code: str
    name: str
    price: float
    stock: int



# ==============================
# PHÂN TÍCH LỖI CODE CŨ
# ==============================
#
# Lỗi logic:
# API cho phép tạo sản phẩm trùng code.
#
# Ví dụ:
#
# Trong database đã có:
#
# {
#   "code": "SP001"
# }
#
# Gửi request:
#
# {
#   "code": "SP001",
#   "name": "Laptop Asus",
#   "price": 20000000,
#   "stock": 5
# }
#
# Code cũ vẫn:
#
# products.append(new_product)
#
# => tạo thêm sản phẩm có code SP001.
#
#
# Nguyên nhân:
# Không kiểm tra code đã tồn tại trước khi thêm.
#
#
# Test case lỗi:
#
# Test 1:
# Input:
# code = "SP001"
#
# Kết quả hiện tại:
# Tạo thành công
#
# Kết quả đúng:
# Báo lỗi code đã tồn tại
#
#
# Test 2:
# Input:
# code = "SP002"
#
# Kết quả hiện tại:
# Tạo thành công
#
# Kết quả đúng:
# Báo lỗi vì SP002 đã tồn tại



# ==============================
# API CREATE PRODUCT
# ==============================

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):


    # Kiểm tra mã sản phẩm bị trùng
    for item in products:

        if item["code"] == product.code:

            raise HTTPException(
                status_code=400,
                detail="Mã sản phẩm đã tồn tại"
            )


    # Tạo sản phẩm mới
    new_product = {

        "id": len(products) + 1,

        "code": product.code,

        "name": product.name,

        "price": product.price,

        "stock": product.stock
    }


    # Thêm vào danh sách
    products.append(new_product)


    return {
        "message": "Create product successfully",
        "data": new_product
    }