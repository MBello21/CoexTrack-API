from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VehicleDetails(BaseModel):
    plate: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    vehicle_type: Optional[str] = None
    engine_type: Optional[str] = None
    odometer: Optional[float] = None

    class Config:
        from_attributes = True


class VehicleSummary(BaseModel):
    plate: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    odometer: Optional[float] = None

    class Config:
        from_attributes = True


class WorkerSummary(BaseModel):
    name: str
    last_name: str
    dni: str

    class Config:
        from_attributes = True


class WorkerDetails(BaseModel):
    category: str
    name: str
    last_name: str
    phone: str
    dni: str
    worker_code_id: str
    start_date: datetime

    class Config:
        from_attributes = True
