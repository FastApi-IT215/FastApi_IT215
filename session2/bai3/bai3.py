from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An", "status": "active"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "active"},
    {"id": 4, "name": "Dung", "status": "pending"}
]

# Phân tích bài toán:
#
# Input:
# - Danh sách sinh viên có sẵn trong biến students.
# - Mỗi sinh viên gồm:
#   id, name, status
#
# Output:
# - Trả về JSON gồm:
#   message: thông báo kết quả
#   data: danh sách sinh viên đang học
#
# Điều kiện xác định sinh viên đang học:
# - status phải bằng "active"
#
# Các bước xử lý API:
# 1. Nhận request GET /students/active
# 2. Duyệt danh sách students
# 3. Lọc các sinh viên có status == "active"
# 4. Kiểm tra kết quả sau khi lọc
# 5. Trả về message và data


# Endpoint đúng theo yêu cầu nghiệp vụ:
# GET /students/active
#
# Không sử dụng:
# - Path parameter
# - Query parameter
# - Request body

@app.get("/students/active")
def get_active_students():

    # Lọc sinh viên đang học
    active_students = []

    for student in students:
        if student["status"] == "active":
            active_students.append(student)

    # Xử lý trường hợp không có sinh viên đang học
    if len(active_students) == 0:
        return {
            "message": "Không có sinh viên đang học",
            "data": []
        }

    # Trả về danh sách sinh viên đang học
    return {
        "message": "Danh sách sinh viên đang học",
        "data": active_students
    }