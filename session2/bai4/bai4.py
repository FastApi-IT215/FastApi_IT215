from fastapi import FastAPI

app = FastAPI()

books = [
    {"id": 1, "title": "Python Basic", "quantity": 12},
    {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
    {"id": 3, "title": "Clean Code", "quantity": 5},
    {"id": 4, "title": "Database Design", "quantity": 0},
    {"id": 5, "title": "Web API Design", "quantity": 20},
    {"id": 6, "title": "Java Basic"},
    {"id": 7, "title": "Spring Boot", "quantity": -2}
]


# Phần 1: Phân tích Input/Output
#
# Input:
# - Danh sách sách books.
# - Mỗi sách gồm:
#   id, title, quantity
#
# Output:
# - JSON gồm:
#   message: thông báo kết quả
#   data: danh sách sách sắp hết hàng
#
# Điều kiện xác định sách sắp hết hàng:
# - quantity <= 5
#
# Các trường hợp cần xử lý:
# - Thiếu quantity -> bỏ qua
# - quantity âm -> dữ liệu không hợp lệ, bỏ qua
# - Không có sách phù hợp -> trả về message và data rỗng


# Phần 2: Các giải pháp lọc dữ liệu
#
# Giải pháp 1: Dùng vòng lặp for
#
# Ưu điểm:
# - Dễ hiểu
# - Dễ xử lý dữ liệu lỗi
# - Dễ bảo trì
#
# Nhược điểm:
# - Code dài hơn
#
#
# Giải pháp 2: Dùng list comprehension
#
# Ví dụ:
# low_stock = [
#     book for book in books
#     if book["quantity"] <= 5
# ]
#
# Ưu điểm:
# - Code ngắn gọn
# - Viết nhanh
#
# Nhược điểm:
# - Khó xử lý trường hợp thiếu quantity
# - Khó đọc khi logic phức tạp
#
#
# Lựa chọn:
# Sử dụng vòng lặp for vì dễ kiểm tra dữ liệu lỗi
# và phù hợp với yêu cầu nghiệp vụ.


# Phần 4: Luồng xử lý API
#
# 1. Khởi tạo FastAPI
# 2. Khai báo danh sách books
# 3. Tạo endpoint GET /books/low-stock
# 4. Duyệt từng sách
# 5. Kiểm tra quantity tồn tại
# 6. Bỏ qua quantity âm
# 7. Lấy sách có quantity <= 5
# 8. Trả về kết quả


@app.get("/books/low-stock")
def get_low_stock_books():

    low_stock_books = []

    for book in books:

        # Bỏ qua sách không có quantity
        if "quantity" not in book:
            continue

        # Bỏ qua dữ liệu quantity âm
        if book["quantity"] < 0:
            continue

        # Lấy sách sắp hết hàng
        if book["quantity"] <= 5:
            low_stock_books.append(book)

    # Không có sách sắp hết hàng
    if len(low_stock_books) == 0:
        return {
            "message": "Không có sách nào sắp hết hàng",
            "data": []
        }

    # Có sách sắp hết hàng
    return {
        "message": "Danh sách sách sắp hết hàng",
        "data": low_stock_books
    }