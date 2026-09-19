from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import model_validator
from geoalchemy2.shape import to_shape

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
    @model_validator(mode="before")
    @classmethod
    def extract_coords(cls, data):
        if hasattr(data, "location") and data.location:
            shape = to_shape(data.location)
            data.lat = shape.y
            data.lon = shape.x
        return data

class TelemetryWithDataOut(TelemetryOut):
    vehicle: Optional[VehicleDetails] = None
    worker: Optional[WorkerSummary] = None

    class Config:
        from_attributes = True 

    @model_validator(mode="before")
    @classmethod
    def extract_relations(cls, data):
        if hasattr(data, "device") and data.device:
            active = [v for v in data.device.vehicle if v.end_date is None]
            if active:
                data.vehicle = active[0]
        if hasattr(data, "session") and data.session:
            data.worker = data.session.worker
        return data



