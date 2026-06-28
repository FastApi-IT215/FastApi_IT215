from fastapi import FastAPI

app = FastAPI()

students = ["An", "Binh", "Cuong"]

# Lỗi cũ:
# Endpoint dùng /getStudents không đúng chuẩn RESTful
# REST nên dùng danh từ đại diện tài nguyên, ví dụ: /students
# Không nên đặt tên endpoint có động từ "get"

# Lỗi cũ:
# return "Danh sach sinh vien: " + str(students)
# str(students) biến list thành chuỗi string
# Frontend không nhận được JSON array để xử lý dữ liệu
# FastAPI có thể tự chuyển list Python thành JSON nên không cần nối chuỗi

# API GET dùng để lấy danh sách toàn bộ sinh viên
@app.get("/students")
def get_students():
    # Trả về trực tiếp list
    # FastAPI tự động chuyển đổi thành JSON array
    return students