from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    total_price: int

    class Config:
        from_attributes = True