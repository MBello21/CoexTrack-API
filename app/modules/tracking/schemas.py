from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from ...shared.schemas import VehicleDetails, WorkerSummary


class TelemetryIn(BaseModel):
    device_id: str
    session_id: Optional[int] = None
    timestamp: datetime
    lat: float
    lon: float
    alt: Optional[float] = None
    speed: Optional[float] = None
    course: Optional[float] = None
    sats: Optional[float] = None
    hdop: Optional[float] = None
    ignition: bool = False
    aspa_active: bool = False
    battery_voltage: Optional[float] = None
    battery_current_ma: Optional[float] = None
    alert: Optional[str] = None


class TelemetryOut(BaseModel):
    device_id: str
    session_id: Optional[int] = None
    timestamp: Optional[datetime] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    alt: Optional[float] = None
    speed: Optional[float] = None
    course: Optional[float] = None
    sats: Optional[float] = None
    hdop: Optional[float] = None
    ignition: Optional[bool] = False
    aspa_active: Optional[bool] = False
    battery_voltage: Optional[float] = None
    battery_current_ma: Optional[float] = None
    alert: Optional[str] = None

    class Config:
        from_attributes = True


class TelemetryWithDataOut(TelemetryOut):
    vehicle: VehicleDetails
    worker: Optional[WorkerSummary]
    

    class Config:
        from_attributes = True 


class TelemetryLatestOut(TelemetryOut):
    plate: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    vehicle_type: Optional[str] = None
    engine_type: Optional[str] = None
