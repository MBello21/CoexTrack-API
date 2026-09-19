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


class VehicleSummary(BaseModel):
    plate: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    odometer: Optional[float] = None


class WorkerSummary(BaseModel):
    name: str
    last_name: str
    dni: str


class WorkerDetails(BaseModel):
    category: str
    name: str
    last_name: str
    phone: str
    dni: str
    worker_code: str
    start_date: datetime
