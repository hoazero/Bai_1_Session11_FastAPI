from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime

class ParkingSlotCreate(BaseModel):
    slot_code: str = Field(..., max_length=50)
    zone_name: str = Field(..., min_length=3, max_length=255)
    max_weight: int = Field(..., gt=0, description="Tải trọng phải lớn hơn 0")
    is_available: Optional[bool] = True

class ParkingSlotResponse(BaseModel):
    id: int
    slot_code: str
    zone_name: str
    max_weight: int
    is_available: bool

    class Config:
        from_attributes = True

class StandardResponse(BaseModel):
    statusCode: int
    message: str
    error: Optional[str] = None
    data: Any
    path: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")