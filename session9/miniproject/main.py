from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field
from typing import Optional, Any, Tuple
from datetime import datetime, timezone

app = FastAPI(title="Team Task Manager API")

class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
    timestamp: str
    path: str

class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=1)
    assignee: str = Field(..., min_length=1)
    priority: int = Field(..., ge=1, le=5)

class TaskStatusUpdateSchema(BaseModel):
    status: str = Field(..., min_length=1)

tasks_db = [
    {
        "id": 1, 
        "title": "Thiet ke database Shop AI", 
        "description": "Xay dung bang va toi uu index", 
        "assignee": "QuyDev", 
        "priority": 1, 
        "status": "todo",
        "created_at": "2026-07-01T09:00:00Z"
    },
    {
        "id": 2, 
        "title": "Code bo API Authen", 
        "description": "Trien khai filter verify JWT token", 
        "assignee": "FixerQ", 
        "priority": 2, 
        "status": "done",
        "created_at": "2026-07-01T10:00:00Z"
    }
]

def get_current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def success_response(status_code: int, message: str, data: Any, request: Request) -> APIResponse:
    return APIResponse(
        statusCode=status_code,
        message=message,
        data=data,
        error=None,
        timestamp=get_current_timestamp(),
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
            "timestamp": get_current_timestamp(),
            "path": request.url.path
        }
    )

def calculate_team_metrics() -> Tuple[int, int, float]:
    total_tasks = len(tasks_db)
    if total_tasks == 0:
        return (0, 0, 0.0)
        
    completed_tasks = 0
    for task in tasks_db:
        if task["status"] == "done":
            completed_tasks += 1
            
    completion_rate_percentage = round((completed_tasks / total_tasks) * 100, 1)
    return (total_tasks, completed_tasks, completion_rate_percentage)

# Chức năng 1: Xem danh sách công việc hiện có
@app.get("/tasks", tags=["Tasks"], response_model=APIResponse)
def get_all_tasks(request: Request, status: Optional[str] = None):
    # Bước 1: Khởi tạo mảng chứa kết quả mặc định lấy từ toàn bộ dữ liệu hệ thống
    filtered_tasks = tasks_db
    
    # Bước 2: Kiểm tra nếu Client có truyền tham số lọc status thì tiến hành duyệt mảng lọc theo trạng thái
    if status is not None:
        filtered_tasks = []
        for task in tasks_db:
            if task["status"].lower() == status.lower():
                filtered_tasks.append(task)
                
    # Bước 3: Đóng gói và trả về kết quả qua hàm success_response (mảng rỗng nếu hệ thống không có dữ liệu phù hợp)
    return success_response(200, "Lấy danh sách công việc thành công!", filtered_tasks, request)

@app.post("/tasks", tags=["Tasks"], status_code=status.HTTP_201_CREATED, response_model=APIResponse)
def create_task(task_in: TaskCreateSchema, request: Request):
    for task in tasks_db:
        if task["title"].strip().lower() == task_in.title.strip().lower():
            raise_business_error(
                status_code=400,
                message="Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!",
                error_code="ERR-TASK-01",
                tech_detail="Task conflict: Title field duplicates an existing record.",
                request=request
            )
            
    max_id = 0
    for task in tasks_db:
        if task["id"] > max_id:
            max_id = task["id"]
            
    new_task = {
        "id": max_id + 1,
        "title": task_in.title.strip(),
        "description": task_in.description.strip(),
        "assignee": task_in.assignee.strip(),
        "priority": task_in.priority,
        "status": "todo",
        "created_at": get_current_timestamp()
    }
    
    tasks_db.append(new_task)
    return success_response(201, "Khởi tạo công việc mới thành công!", new_task, request)

@app.put("/tasks/{task_id}", tags=["Tasks"], response_model=APIResponse)
def update_task_status(task_id: int, status_in: TaskStatusUpdateSchema, request: Request):
    target_task = None
    for task in tasks_db:
        if task["id"] == task_id:
            target_task = task
            break
            
    if target_task is None:
        raise_business_error(
            status_code=404,
            message="Lỗi: Không tìm thấy mã công việc yêu cầu cập nhật tiến độ!",
            error_code="ERR-TASK-03",
            tech_detail="Resource update failure: Target task ID can not be found in active memory database array.",
            request=request
        )
        
    if target_task["status"].lower() == "done":
        raise_business_error(
            status_code=400,
            message="Lỗi: Công việc này đã hoàn thành từ trước, không được phép thay đổi trạng thái!",
            error_code="ERR-TASK-04",
            tech_detail="Business validation error: Final state reached. Modifications to completed tasks are strongly restricted.",
            request=request
        )
        
    target_task["status"] = status_in.status.strip()
    return success_response(200, "Cập nhật tiến độ công việc thành công!", target_task, request)

@app.get("/tasks/analytics/dashboard", tags=["Analytics"], response_model=APIResponse)
def get_dashboard_analytics(request: Request):
    total_tasks, completed_tasks, completion_rate_percentage = calculate_team_metrics()
    
    analytics_data = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate_percentage": completion_rate_percentage
    }
    
    return success_response(200, "Lấy số liệu thống kê hiệu suất nhóm thành công!", analytics_data, request)

@app.exception_handler(HTTPException)
def custom_http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and "statusCode" in exc.detail:
        return exc.detail
    return {
        "statusCode": exc.status_code,
        "message": "Yêu cầu xử lý gặp lỗi hệ thống!",
        "data": None,
        "error": f"ERR-HTTP: {str(exc.detail)}",
        "timestamp": get_current_timestamp(),
        "path": request.url.path
    }

@app.exception_handler(422)
def validation_exception_handler(request: Request, exc: Any):
    return {
        "statusCode": 422,
        "message": "Lỗi: Dữ liệu đầu vào không hợp lệ hoặc sai định dạng quy định!",
        "data": None,
        "error": "ERR-VAL-422: Validation error at Request Body fields constraint layout.",
        "timestamp": get_current_timestamp(),
        "path": request.url.path
    }

@app.exception_handler(Exception)
def global_runtime_exception_handler(request: Request, exc: Exception):
    return {
        "statusCode": 500,
        "message": "Lỗi hệ thống: Đã xảy ra lỗi không mong muốn trên máy chủ, vui lòng thử lại sau!",
        "data": None,
        "error": f"ERR-SERVER-500: Internal server runtime error crash caught.",
        "timestamp": get_current_timestamp(),
        "path": request.url.path
    }