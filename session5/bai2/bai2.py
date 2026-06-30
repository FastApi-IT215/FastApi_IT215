from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI()


enrollments = [
    {
        "id": 1,
        "student_id": "SV001",
        "course_id": 1
    },
    {
        "id": 2,
        "student_id": "SV002",
        "course_id": 1
    }
]


# Model nhận dữ liệu đăng ký khóa học
class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: int



# ==============================
# PHÂN TÍCH LỖI CODE CŨ
# ==============================
#
# Lỗi logic:
# API cho phép một học viên đăng ký cùng một khóa học nhiều lần.
#
#
# Ví dụ dữ liệu đã có:
#
# {
#   "student_id": "SV001",
#   "course_id": 1
# }
#
#
# Gửi tiếp:
#
# {
#   "student_id": "SV001",
#   "course_id": 1
# }
#
#
# Code cũ vẫn:
#
# enrollments.append(new_enrollment)
#
# => tạo thêm bản ghi trùng.
#
#
# Nguyên nhân:
# Không kiểm tra student_id và course_id
# đã tồn tại trước khi thêm.
#
#
# Test case lỗi:
#
# Test 1:
#
# Input:
# student_id = "SV001"
# course_id = 1
#
# Kết quả hiện tại:
# Vẫn đăng ký thành công
#
# Kết quả đúng:
# Báo lỗi học viên đã đăng ký khóa học này
#
#
# Test 2:
#
# Input:
# student_id = "SV002"
# course_id = 1
#
# Kết quả hiện tại:
# Vẫn tạo thêm bản ghi
#
# Kết quả đúng:
# Báo lỗi đăng ký trùng
#



# ==============================
# API CREATE ENROLLMENT
# ==============================

@app.post("/enrollments", status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: EnrollmentCreate):


    # Kiểm tra đăng ký trùng
    for item in enrollments:


        if (
            item["student_id"] == enrollment.student_id
            and item["course_id"] == enrollment.course_id
        ):

            raise HTTPException(
                status_code=400,
                detail="Học viên đã đăng ký khóa học này"
            )


    # Tạo đăng ký mới
    new_enrollment = {

        "id": len(enrollments) + 1,

        "student_id": enrollment.student_id,

        "course_id": enrollment.course_id
    }


    # Thêm vào danh sách
    enrollments.append(new_enrollment)


    return {
        "message": "Enroll successfully",
        "data": new_enrollment
    }