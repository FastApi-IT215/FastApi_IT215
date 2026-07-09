from pydantic import BaseModel, Field
from typing import Optional, Literal

class BoardingSlotCreateDTO(BaseModel):
    slot_number: str
    room_size: Literal["SMALL", "MEDIUM", "LARGE"]
    price_per_day: float = Field(gt=0)
    status: Literal["VACANT", "OCCUPIED"] = "VACANT"

class BoardingSlotUpdateDTO(BaseModel):
    slot_number: Optional[str] = None
    room_size: Optional[Literal["SMALL", "MEDIUM", "LARGE"]] = None
    price_per_day: Optional[float] = Field(default=None, gt=0)
    status: Optional[Literal["VACANT", "OCCUPIED"]] = None

class BoardingSlotResponseDTO(BaseModel):
    id: int
    slot_number: str
    room_size: str
    price_per_day: float
    status: str

    class Config:
        from_attributes = True