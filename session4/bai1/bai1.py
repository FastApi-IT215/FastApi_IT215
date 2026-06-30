from fastapi import FastAPI

app = FastAPI()


products = [
    {"id": 1, "name": "Laptop Dell", "price": 15000000},
    {"id": 2, "name": "Chuột Logitech", "price": 350000},
    {"id": 3, "name": "Bàn phím cơ", "price": 1200000}
]


# ==========================
# PHÂN TÍCH LỖI CODE CŨ
# ==========================
#
# Lỗi 1:
# Khi gọi:
# GET /products/1
#
# API trả về 404 Not Found
# vì route cũ là:
#
# @app.get("/products/product_id")
#
# FastAPI hiểu đây là đường dẫn cố định:
#
# /products/product_id
#
# chứ không phải biến product_id.
#
#
# Lỗi 2:
# Dòng khai báo sai Path Parameter:
#
# @app.get("/products/product_id")
#
# Muốn tạo Path Parameter phải dùng dấu {}:
#
# /products/{product_id}
#
#
# Lỗi 3:
# /products/product_id không phải Path Parameter
# vì "product_id" chỉ là chữ bình thường trong URL.
#
# FastAPI không lấy được giá trị từ URL.
#
# Ví dụ:
#
# /products/product_id
#
# nghĩa là chỉ có đúng URL này.
#
# Còn:
#
# /products/1
#
# sẽ không khớp.
#
#
# Endpoint đúng:
#
# GET /products/{product_id}
#
# Ví dụ:
#
# GET /products/1
# GET /products/2
#
# FastAPI sẽ truyền số 1, 2 vào biến product_id.


# ==========================
# API LẤY CHI TIẾT SẢN PHẨM
# ==========================

@app.get("/products/{product_id}")
def get_product_detail(product_id: int):

    # Duyệt danh sách sản phẩm
    for product in products:

        # Kiểm tra id sản phẩm
        if product["id"] == product_id:

            # Trả về sản phẩm tìm thấy
            return product


    # Không tìm thấy sản phẩm
    return {
        "message": "Không tìm thấy sản phẩm"
    }