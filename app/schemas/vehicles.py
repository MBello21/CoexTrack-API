from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VehicleIn(BaseModel):

    vehicle_id: str
    plate: str
    brand: str
    model: str
    vehicle_type: str
    driver: Optional[str] = None
    engine_type: str


class VehicleOut(BaseModel):

    id: int
    vehicle_id: str
    plate: str
    brand: str
    model: str
    vehicle_type: str
    driver: Optional[str] = None
    engine_type: str

    class Config:
        from_attributes = True
