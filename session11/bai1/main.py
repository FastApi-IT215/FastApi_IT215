from datetime import datetime, timezone

from fastapi import FastAPI, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import Base, engine, get_db
from models import ParkingSlot
from schemas import ParkingSlotCreate

app = FastAPI(
    title="Parking Lot Management API",
    description="API Quản lý vị trí xe công nghệ tại bãi đỗ"
)

Base.metadata.create_all(bind=engine)


@app.post("/parking-slots", status_code=status.HTTP_201_CREATED)
def create_parking_slot(
    parking_slot: ParkingSlotCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        new_slot = ParkingSlot(
            slot_code=parking_slot.slot_code,
            zone_name=parking_slot.zone_name,
            max_weight=parking_slot.max_weight
        )

        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)

        return {
            "statusCode": 201,
            "message": "Thêm vị trí đỗ xe thành công",
            "error": None,
            "data": {
                "id": new_slot.id,
                "slot_code": new_slot.slot_code,
                "zone_name": new_slot.zone_name,
                "max_weight": new_slot.max_weight,
                "is_available": new_slot.is_available
            },
            "path": str(request.url.path),
            "timestamp": datetime.now(timezone.utc)
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="slot_code đã tồn tại"
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Lỗi cơ sở dữ liệu"
        )


@app.get("/parking-slots")
def get_all_slots(
    request: Request,
    db: Session = Depends(get_db)
):
    slots = db.query(ParkingSlot).all()

    data = []

    for slot in slots:
        data.append({
            "id": slot.id,
            "slot_code": slot.slot_code,
            "zone_name": slot.zone_name,
            "max_weight": slot.max_weight,
            "is_available": slot.is_available
        })

    return {
        "statusCode": 200,
        "message": "Lấy danh sách vị trí đỗ xe thành công",
        "error": None,
        "data": data,
        "path": str(request.url.path),
        "timestamp": datetime.now(timezone.utc)
    }


@app.get("/parking-slots/{slot_id}")
def get_slot_detail(
    slot_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()

    if slot is None:
        raise HTTPException(
            status_code=404,
            detail="Parking slot not found"
        )

    return {
        "statusCode": 200,
        "message": "Lấy thông tin vị trí đỗ xe thành công",
        "error": None,
        "data": {
            "id": slot.id,
            "slot_code": slot.slot_code,
            "zone_name": slot.zone_name,
            "max_weight": slot.max_weight,
            "is_available": slot.is_available
        },
        "path": str(request.url.path),
        "timestamp": datetime.now(timezone.utc)
    }





    