from sqlalchemy import Column, Integer, String
from database import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100))
    total_price = Column(Integer)