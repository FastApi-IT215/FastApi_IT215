from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import MenuItemCreateDTO, MenuItemUpdateDTO
from models import MenuItem

def create_menu_item(db: Session, item: MenuItemCreateDTO):
    try:
        new_item = MenuItem(
            dish_code = item.dish_code,
            dish_name = item.dish_name,
            calorie_count = item.calorie_count,
            price = item.price,
            status = item.status
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError as s:
        db.rollback()
        raise s

def get_menu_item(db: Session, item_id: int):
    return db.query(MenuItem).filter(MenuItem.id == item_id).first()

def get_all_menu_items(db: Session):
    return db.query(MenuItem).all()

def update_menu_item(db: Session, item_id: int, item: MenuItemUpdateDTO):
    try:
        db_item = get_menu_item(db, item_id)
        if not db_item:
            return None
        update_data = item.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item
    except IntegrityError:
        db.rollback()
        raise
    except SQLAlchemyError as s:
        db.rollback()
        raise s

def delete_menu_item(db: Session, item_id: int):
    try:
        db_item = get_menu_item(db, item_id)
        if not db_item:
            return None
        db.delete(db_item)
        db.commit()
        return db_item
    except SQLAlchemyError as s:
        db.rollback()
        raise s
