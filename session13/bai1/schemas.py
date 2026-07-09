from pydantic import BaseModel, Field
from typing import Optional, Literal

class MenuItemCreateDTO(BaseModel):
    dish_code: str
    dish_name: str = Field(min_length=1)
    calorie_count: int = Field(gt=0)
    price: float = Field(gt=0)
    status: Literal["AVAILABLE", "OUT_OF_STOCK"] = "AVAILABLE"

class MenuItemUpdateDTO(BaseModel):
    dish_code: Optional[str] = None
    dish_name: Optional[str] = Field(default=None, min_length=1)
    calorie_count: Optional[int] = Field(default=None, gt=0)
    price: Optional[float] = Field(default=None, gt=0)
    status: Optional[Literal["AVAILABLE", "OUT_OF_STOCK"]] = None

class MenuItemResponseDTO(BaseModel):
    id: int
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: str

    class Config:
        from_attributes = True