# schemas/telemetry.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TelemetryIn(BaseModel):
    vehicle_id: str
    timestamp: datetime
    lat: float
    lon: float
    alt: Optional[float] = None
    speed: Optional[float] = None
    course: Optional[float] = None
    sats: Optional[int] = None
    hdop: Optional[float] = None
    ignition: bool = True


class TelemetryOut(BaseModel):
    vehicle_id: str
    timestamp: datetime
    lat: float
    lon: float
    alt: Optional[float] = None
    speed: Optional[float] = None
    course: Optional[float] = None
    sats: Optional[int] = None
    hdop: Optional[float] = None
    ignition: bool

    class Config:
        from_attributes = True