from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import BoardingSlotCreateDTO, BoardingSlotUpdateDTO
from models import BoardingSlot

def create_slot(db: Session, slot: BoardingSlotCreateDTO):
    try:
        new_slot = BoardingSlot(
            slot_number = slot.slot_number,
            room_size = slot.room_size,
            price_per_day = slot.price_per_day,
            status = slot.status
        )
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
        return new_slot
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError as s:
        db.rollback()
        raise s

def get_slot(db: Session, slot_id: int):
    return db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()

def get_all_slots(db: Session):
    return db.query(BoardingSlot).all()

def update_slot(db: Session, slot_id: int, slot: BoardingSlotUpdateDTO):
    try:
        db_slot = get_slot(db, slot_id)
        if not db_slot:
            return None
        update_data = slot.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_slot, key, value)
        db.commit()
        db.refresh(db_slot)
        return db_slot
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError as s:
        db.rollback()
        raise s

def delete_slot(db: Session, slot_id: int):
    try:
        db_slot = get_slot(db, slot_id)
        if not db_slot:
            return None
        db.delete(db_slot)
        db.commit()
        return db_slot
    except SQLAlchemyError as s:
        db.rollback()
        raise s
