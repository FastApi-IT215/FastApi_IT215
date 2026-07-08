from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import CustomerModel
from schemas import CustomerUpdate

app = FastAPI(
    title="Customer Manager"
)

Base.metadata.create_all(bind=engine)


@app.put("/customers/{customer_id}", status_code=status.HTTP_200_OK)
def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db)
):
    customer = db.query(CustomerModel).filter(
        CustomerModel.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    customer.full_name = customer_update.full_name
    customer.phone = customer_update.phone
    customer.address = customer_update.address

    db.commit()
    db.refresh(customer)

    return {
        "status_code": 200,
        "message": "Customer updated successfully",
        "data": {
            "id": customer.id,
            "full_name": customer.full_name,
            "phone": customer.phone,
            "address": customer.address
        }
    }