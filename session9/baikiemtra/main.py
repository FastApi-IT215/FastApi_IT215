from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime, timezone

app = FastAPI(title="Elearning Course API")

class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
    timestamp: str
    path: str

def success_response(status_code: int, message: str, data: Any, request: Request):
    return APIResponse(
        statusCode=status_code,
        message=message,
        data=data,
        error=None,
        timestamp=datetime.now(timezone.utc).isoformat(),
        path=request.url.path
    )

def raise_business_error(status_code: int, message: str, error_code: str, tech_detail: str, request: Request):
    raise HTTPException(
        status_code=status_code,
        detail={
            "statusCode": status_code,
            "message": message,
            "data": None,
            "error": f"{error_code}: {tech_detail}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": request.url.path
        }
    )

class CourseCreateSchema(BaseModel):
    course_name: str = Field(..., min_length=5)
    duration_hours: int = Field(..., gt=0)
    price: int = Field(..., ge=0)

courses_db = [
    {"id": 1, "course_name": "FastAPI Masterclass", "duration_hours": 32, "price": 1500000, "status": "active", "created_at": "2026-07-01T02:00:00Z"},
    {"id": 2, "course_name": "NextJS Next-Level", "duration_hours": 45, "price": 1800000, "status": "active", "created_at": "2026-07-01T03:15:00Z"}
]

@app.get("/courses", tags=["Courses"], response_model=APIResponse)
def get_all_courses(request: Request):
    return success_response(200, "Lấy danh sách khóa học thành công!", courses_db, request)

@app.post("/courses", tags=["Courses"], status_code=status.HTTP_201_CREATED, response_model=APIResponse)
def create_course(course_data: CourseCreateSchema, request: Request):
    for course in courses_db:
        if course["course_name"].lower() == course_data.course_name.lower():
            raise_business_error(
                status_code=400,
                message="Lỗi: Tên khóa học này đã tồn tại trong danh mục đào tạo!",
                error_code="ERR-EDU-01",
                tech_detail="Course name duplicates an existing record in memory array.",
                request=request
            )
            
    next_id = 1
    for course in courses_db:
        if course["id"] >= next_id:
            next_id = course["id"] + 1
            
    new_course = {
        "id": next_id,
        "course_name": course_data.course_name,
        "duration_hours": course_data.duration_hours,
        "price": course_data.price,
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }
    
    courses_db.append(new_course)
    return success_response(201, "Tạo mới khóa học thành công!", new_course, request)

# @app.delete("/courses/{course_id}", tags=["Courses"], response_model=APIResponse)
# def delete_course(course_id: int, request: Request):
#     target_index = -1
#     for i in range(len(courses_db)):
#         if courses_db[i]["id"] == course_id:
#             target_index = i
  

