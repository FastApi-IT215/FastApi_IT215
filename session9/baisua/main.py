from fastapi import FastAPI, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime, timezone

app = FastAPI(
    title= "Elearning course API",
    description= "API hệ thống khóa học trực tuyến"
)

class APIresponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
    timestamp: str
    path: str

def success_response(statusCode: int, message: str, data: Any, request: Request):
    return APIresponse(
        statusCode= statusCode,
        message= message,
        data= data,
        error= None,
        timestamp= datetime.now(timezone.utc).isoformat(),
        path= request.url.path
    )

courses_db = [
    {"id": 1, "course_name": "FastAPI Masterclass", "duration_hours": 32, "price": 1500000, "status": "active", "created_at": "2026-07-01T02:00:00Z"},
    {"id": 2, "course_name": "NextJS Next-Level", "duration_hours": 45, "price": 1800000, "status": "active", "created_at": "2026-07-01T03:15:00Z"}
]


@app.get("/courses", tags=["Courses"], response_model= APIresponse)
def get_courses(request: Request):
    if not 
    return success_response(200, "Lấy danh sách khóa học thành công!", courses_db, request)