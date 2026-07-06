from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime, timezone

app = FastAPI(title="Team Task Manager API")

# Cấu trúc phản hồi chuẩn (Unified Envelope)
class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any]
    error: Optional[Any]
    timestamp: str
    path: str

# Hàm bổ trợ tạo phản hồi thành công nhanh
def success_response(statusCode: int, message: str, data: Any, request: Request):
    return APIResponse(
        statusCode=statusCode,
        message=message,
        data=data,
        error=None,
        timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        path=request.url.path
    )

# Hàm bổ trợ tạo phản hồi lỗi nhanh theo mã đặc tả
def raise_business_error(statusCode: int, message: str, error_code: str, tech_detail: str, request: Request):
    raise HTTPException(
        status_code=statusCode,
        detail={
            "statusCode": statusCode,
            "message": message,
            "data": None,
            "error": f"{error_code}: {tech_detail}",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "path": request.url.path
        }
    )

# Schema tiếp nhận dữ liệu cập nhật từ Client
class TaskUpdateSchema(BaseModel):
    title: str
    description: str
    assignee: str
    priority: int
    status: str

# Giả lập Cơ sở dữ liệu lưu trữ nội bộ (tasks_db)
tasks_db = [
    {
        "id": 1,
        "title": "Thiết kế cơ sở dữ liệu Shop AI",
        "description": "Xây dựng các lưu trữ bảng và stored procedure tối ưu hóa index",
        "assignee": "QuyDev",
        "priority": 1,
        "status": "todo",
        "created_at": "2026-07-01T09:50:00Z",
        "internal_notes": "Dự án bảo mật cao"
    }
]

# ROUTER XỬ LÝ CHÍNH CHO PHẦN CẬP NHẬT (PUT)
@app.put("/tasks/{task_id}", tags=["Tasks"], response_model=APIResponse)
def update_task(task_id: int, task_data: TaskUpdateSchema, request: Request):
    
    # Bước 1: Tìm vị trí công việc theo ID trong hệ thống
    target_task = None
    for task in tasks_db:
        if task["id"] == task_id:
            target_task = task
            break
            
    # Bước 2: Kiểm tra nếu ID không tồn tại -> Trả lỗi ERR-TASK-04
    if target_task is None:
        raise_business_error(
            statusCode=404,
            message="Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!",
            error_code="ERR-TASK-04",
            tech_detail="Resource missing error: Target task entity parameter [task_id] can not be located within current active database scope.",
            request=request
        )
        
    # Bước 3: Kiểm tra tính hợp lệ của độ dài ký tự Title (từ 3 đến 150 ký tự)
    if len(task_data.title) < 3 or len(task_data.title) > 150:
        raise_business_error(
            statusCode=422,
            message="Lỗi: Dữ liệu đầu vào sai định dạng hoặc thiếu trường bắt buộc!",
            error_code="ERR-VAL-422",
            tech_detail="Gateway validation error: Title length must be between 3 and 150 characters.",
            request=request
        )

    # Bước 4: Kiểm tra điều kiện biên của độ ưu tiên Priority (phải từ 1 đến 5) -> Trả lỗi ERR-TASK-02
    if task_data.priority < 1 or task_data.priority > 5:
        raise_business_error(
            statusCode=422,
            message="Lỗi: Mức độ ưu tiên công việc không hợp lệ (Phải từ 1 đến 5)!",
            error_code="ERR-TASK-02",
            tech_detail="Validation error: Priority field numerical bounds limits constraint violation. Value must be ge=1 and le=5.",
            request=request
        )
        
    # Bước 5: Kiểm tra logic danh sách trạng thái Status cho phép -> Trả lỗi ERR-TASK-03
    if task_data.status not in ["todo", "in_progress", "done"]:
        raise_business_error(
            statusCode=400,
            message="Lỗi: Trạng thái công việc cập nhật không đúng quy định!",
            error_code="ERR-TASK-03",
            tech_detail="Business logic error: Invalid task status value. Allowed enumerated selection list: ['todo', 'in_progress', 'done'].",
            request=request
        )

    # Bước 6: Tiến hành cập nhật đè dữ liệu mới (Giữ nguyên id và created_at gốc)
    target_task["title"] = task_data.title
    target_task["description"] = task_data.description
    target_task["assignee"] = task_data.assignee
    target_task["priority"] = task_data.priority
    target_task["status"] = task_data.status

    # Bước 7: Trích xuất ra lớp bảo mật (loại bỏ trường internal_notes trước khi trả ra client)
    public_response_data = {
        "id": target_task["id"],
        "title": target_task["title"],
        "description": target_task["description"],
        "assignee": target_task["assignee"],
        "priority": target_task["priority"],
        "status": target_task["status"],
        "created_at": target_task["created_at"]
    }

    # Bước 8: Trả về kết quả thành công mã 200 OK bọc qua lớp Envelope chung
    return success_response(200, "Cập nhật tiến độ & Nội dung công việc thành công!", public_response_data, request)