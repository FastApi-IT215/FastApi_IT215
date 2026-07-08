from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import ProductModel
from schemas import ProductCreate

app = FastAPI(
    title="Product API",
    description="API tạo mới sản phẩm"
)

Base.metadata.create_all(bind=engine)


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        new_product = ProductModel(
            sku=product.sku,
            name=product.name,
            price=product.price
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return {
            "message": "Product created successfully",
            "data": {
                "id": new_product.id,
                "sku": new_product.sku,
                "name": new_product.name,
                "price": new_product.price
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi tạo sản phẩm: {str(e)}"
        )