from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product_data: ProductCreate):
    new_product = Product(name=product_data.name, price=product_data.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    product = get_product_by_id(db, product_id)
    if product is None:
        return None
    product.name = product_data.name
    product.price = product_data.price
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if product is None:
        return None
    db.delete(product)
    db.commit()
    return product
