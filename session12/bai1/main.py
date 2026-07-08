from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import ProductModel
from schemas import ProductUpdate

app = FastAPI(
    title="Product API",
    description="API cập nhật sản phẩm"
)

Base.metadata.create_all(bind=engine)


@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    product.name = product_update.name
    product.price = product_update.price

    db.commit()
    db.refresh(product)

    return {
        "message": "Product updated successfully",
        "data": {
            "id": product.id,
            "sku": product.sku,
            "name": product.name,
            "price": product.price
        }
    }