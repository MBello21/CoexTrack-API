from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VehicleIn(BaseModel):

    device_id: str
    plate: str
    brand: str
    model: str
    vehicle_type: str
    driver: Optional[str] = None
    engine_type: str
    start_date: datetime


class VehicleOut(BaseModel):

    id: int
    device_id: str
    plate: str
    brand: str
    model: str
    vehicle_type: str
    driver: Optional[str] = None
    engine_type: str
    start_date: datetime
    end_date: Optional[datetime] = None

    class Config:
        from_attributes = True
