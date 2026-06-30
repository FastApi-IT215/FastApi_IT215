from fastapi import FastAPI

app = FastAPI()


orders = [
    {
        "id": 1,
        "customer_name": "Nguyễn Văn An",
        "total": 250000,
        "status": "pending"
    },
    {
        "id": 2,
        "customer_name": "Trần Thị Bình",
        "total": 500000,
        "status": "paid"
    },
    {
        "id": 3,
        "customer_name": "Lê Văn Cường",
        "total": 150000,
        "status": "cancelled"
    },
    {
        "id": 4,
        "customer_name": "Phạm Thị Dung",
        "total": 320000,
        "status": "pending"
    }
]


# ==========================
# PHÂN TÍCH LỖI
# ==========================
#
# 1. Endpoint hiện tại có Path Parameter không?
#
# Có.
#
# Endpoint:
#
# /orders/status/{status}
#
# có Path Parameter là:
#
# {status}
#
#
# 2. Path Parameter trong bài này là gì?
#
# Là:
#
# status
#
# Dùng để nhận trạng thái đơn hàng từ URL.
#
#
# Ví dụ:
#
# GET /orders/status/pending
#
# thì status = "pending"
#
#
# 3. Khi gọi /orders/status/pending,
# biến status nhận giá trị gì?
#
# status nhận:
#
# "pending"
#
#
# 4. Vì sao API hiện tại trả về sai dữ liệu?
#
# Vì trong hàm:
#
# return orders
#
# trả về toàn bộ danh sách orders
# mà không kiểm tra giá trị status.
#
#
# 5. Dòng code khiến API bỏ qua status:
#
# return orders
#
# Vì dòng này không sử dụng biến:
#
# status
#
# để lọc dữ liệu.


# ==========================
# API LỌC ĐƠN HÀNG THEO STATUS
# ==========================

@app.get("/orders/status/{status}")
def get_orders_by_status(status: str):

    # Danh sách trạng thái hợp lệ
    valid_status = [
        "pending",
        "paid",
        "cancelled"
    ]


    # Kiểm tra trạng thái có hợp lệ không
    if status not in valid_status:

        return {
            "message": "Trạng thái đơn hàng không hợp lệ"
        }


    # Danh sách kết quả
    result = []


    # Duyệt từng đơn hàng
    for order in orders:


        # Kiểm tra trạng thái đơn hàng
        if order["status"] == status:

            # Thêm đơn hàng phù hợp
            result.append(order)


    # Trả về danh sách JSON
    return result