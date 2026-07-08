from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import OrderModel

app = FastAPI(
    title="Order API",
    description="API lấy thông tin đơn hàng"
)

Base.metadata.create_all(bind=engine)


@app.get("/orders/{order_id}")
def get_order_detail(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return {
        "id": order.id,
        "customer_name": order.customer_name,
        "total_price": order.total_price
    }