from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from database import get_db, Base, engine
from schemas import BoardingSlotCreateDTO, BoardingSlotUpdateDTO, BoardingSlotResponseDTO
import boarding_services

app = FastAPI(
    title = "Pet Boarding Slots Management"
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

@app.post("/boarding-slots", tags=["BoardingSlots"])
def add_slot(slot: BoardingSlotCreateDTO, request: Request, db: Session = Depends(get_db)):
    try:
        db_slot = boarding_services.create_slot(db, slot)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Slot number already exists")
    data = BoardingSlotResponseDTO.model_validate(db_slot).model_dump()
    return build_response(201, "Thêm khoang lưu trú thành công", None, data, str(request.url.path))

@app.get("/boarding-slots", tags=["BoardingSlots"])
def get_all_slots(request: Request, db: Session = Depends(get_db)):
    slots = boarding_services.get_all_slots(db)
    data = [BoardingSlotResponseDTO.model_validate(s).model_dump() for s in slots]
    return build_response(200, "Lấy danh sách thành công", None, data, str(request.url.path))

@app.get("/boarding-slots/{slot_id}", tags=["BoardingSlots"])
def get_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    db_slot = boarding_services.get_slot(db, slot_id)
    if not db_slot:
        raise HTTPException(status_code=404, detail="Boarding slot not found")
    data = BoardingSlotResponseDTO.model_validate(db_slot).model_dump()
    return build_response(200, "Lấy thông tin thành công", None, data, str(request.url.path))

@app.put("/boarding-slots/{slot_id}", tags=["BoardingSlots"])
def update_slot(slot_id: int, slot: BoardingSlotUpdateDTO, request: Request, db: Session = Depends(get_db)):
    try:
        db_slot = boarding_services.update_slot(db, slot_id, slot)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Slot number already exists")
    if not db_slot:
        raise HTTPException(status_code=404, detail="Boarding slot not found")
    data = BoardingSlotResponseDTO.model_validate(db_slot).model_dump()
    return build_response(200, "Cập nhật thành công", None, data, str(request.url.path))

@app.delete("/boarding-slots/{slot_id}", tags=["BoardingSlots"])
def delete_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    db_slot = boarding_services.delete_slot(db, slot_id)
    if not db_slot:
        raise HTTPException(status_code=404, detail="Boarding slot not found")
    return build_response(200, "Xóa thành công", None, None, str(request.url.path))
