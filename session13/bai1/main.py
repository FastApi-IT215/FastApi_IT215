from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from database import get_db, Base, engine
from schemas import MenuItemCreateDTO, MenuItemUpdateDTO, MenuItemResponseDTO
import menu_services

app = FastAPI(
    title = "Catering Menu Management"
)

Base.metadata.create_all(bind = engine)

def build_response(status_code, message, error, data, path):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code = exc.status_code,
        content = build_response(exc.status_code, exc.detail, "Error", None, str(request.url.path))
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code = 422,
        content = build_response(422, "Dữ liệu không hợp lệ", str(exc.errors()), None, str(request.url.path))
    )

@app.post("/menu-items", tags=["MenuItems"])
def add_menu_item(item: MenuItemCreateDTO, request: Request, db: Session = Depends(get_db)):
    try:
        db_item = menu_services.create_menu_item(db, item)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="dish_code đã tồn tại")
    data = MenuItemResponseDTO.model_validate(db_item).model_dump()
    return build_response(201, "Thêm món ăn thành công", None, data, str(request.url.path))

@app.get("/menu-items", tags=["MenuItems"])
def get_all_menu_items(request: Request, db: Session = Depends(get_db)):
    items = menu_services.get_all_menu_items(db)
    data = [MenuItemResponseDTO.model_validate(i).model_dump() for i in items]
    return build_response(200, "Lấy danh sách món ăn thành công", None, data, str(request.url.path))

@app.get("/menu-items/{item_id}", tags=["MenuItems"])
def get_menu_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    db_item = menu_services.get_menu_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    data = MenuItemResponseDTO.model_validate(db_item).model_dump()
    return build_response(200, "Lấy thông tin món ăn thành công", None, data, str(request.url.path))

@app.put("/menu-items/{item_id}", tags=["MenuItems"])
def update_menu_item(item_id: int, item: MenuItemUpdateDTO, request: Request, db: Session = Depends(get_db)):
    try:
        db_item = menu_services.update_menu_item(db, item_id, item)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="dish_code đã tồn tại")
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    data = MenuItemResponseDTO.model_validate(db_item).model_dump()
    return build_response(200, "Cập nhật món ăn thành công", None, data, str(request.url.path))

@app.delete("/menu-items/{item_id}", tags=["MenuItems"])
def delete_menu_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    db_item = menu_services.delete_menu_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return build_response(200, "Xóa món ăn thành công", None, None, str(request.url.path))