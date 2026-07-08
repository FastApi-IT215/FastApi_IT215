from pydantic import BaseModel


class CustomerUpdate(BaseModel):
    full_name: str
    phone: str
    address: str