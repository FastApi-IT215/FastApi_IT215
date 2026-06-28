from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An"},
    {"id": 2, "name": "Binh"},
    {"id": 3, "name": "Cuong"}
]

# Phân tích lỗi code cũ:
#
# Lỗi 1:
# Endpoint cũ là:
# @app.get("/student")
#
# Nhưng yêu cầu của hệ thống là:
# GET /students
#
# Khi gọi GET /students sẽ bị lỗi 404 Not Found
# vì FastAPI không tìm thấy route /students.
#
# Lỗi 2:
# Tên endpoint /student chưa đúng ý nghĩa nghiệp vụ.
# /student là dạng số ít, phù hợp lấy một sinh viên.
# /students là dạng số nhiều, dùng để lấy danh sách nhiều sinh viên.
#
# Lỗi 3:
# return students[0]
#
# Chỉ trả về phần tử đầu tiên trong danh sách.
# Kết quả chỉ có sinh viên:
# {"id":1,"name":"An"}
#
# Không đáp ứng yêu cầu trả về toàn bộ danh sách sinh viên.
#
# Sửa lỗi:
# - Đổi endpoint thành /students
# - Trả về trực tiếp biến students
# - FastAPI tự chuyển list Python thành JSON


@app.get("/students")
def get_students():
    return students