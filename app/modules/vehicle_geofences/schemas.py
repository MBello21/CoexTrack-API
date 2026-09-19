from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VehicleGeofenceIn(BaseModel):
    vehicle_id: int
    geofence_id: int
    alert_on_enter: bool
    alert_on_exit: bool


class VehicleGeofenceOut(BaseModel):
    id: int
    vehicle_id: int
    geofence_id: int
    alert_on_enter: bool
    alert_on_exit: bool

    class Config:
        from_attributes = True