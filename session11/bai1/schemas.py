from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class ParkingSlotCreate(BaseModel):
    slot_code: str
    zone_name: str = Field(min_length=3)
    max_weight: int = Field(gt=0)


class APIResponse(BaseModel):
    statusCode: int
    message: str
    error: Optional[Any] = None
    data: Optional[Any] = None
    path: str
    timestamp: datetime