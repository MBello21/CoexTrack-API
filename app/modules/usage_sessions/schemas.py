from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from .enum import StatusEnum, EndReason
from ...shared.schemas import VehicleSummary, VehicleDetails, WorkerDetails, WorkerSummary


class UsageSessionIn(BaseModel):

    vehicle_id: int
    worker_id: int
    start_odometer: float
    start_location: str
    trip_purpose: Optional[str]
    pre_check_notes: Optional[str]


class UsageSessionEnd(BaseModel):

    end_odometer: float
    end_location: str
    end_reason: EndReason


class UsageSessionOut(BaseModel):
    id: int
    vehicle: VehicleSummary
    worker: WorkerSummary
    device_id: str
    status: StatusEnum
    start_time: datetime
    start_odometer: float
    start_location: str
    trip_purpose: Optional[str]
    pre_check_notes: Optional[str]
    end_time: Optional[datetime]
    end_odometer: Optional[float]
    end_location: Optional[str]
    total_km: Optional[float]
    total_seconds: Optional[int]
    end_reason: Optional[EndReason]
    created_at: datetime

    class Config:
        from_attributes = True


class UsageSessionsWithData(BaseModel):
    id: int
    vehicle: VehicleDetails
    worker: WorkerDetails
    device_id: str
    status: StatusEnum
    start_time: datetime
    start_odometer: float
    start_location: str
    trip_purpose: Optional[str]
    pre_check_notes: Optional[str]
    end_time: Optional[datetime]
    end_odometer: Optional[float]
    end_location: Optional[str]
    total_km: Optional[float]
    total_seconds: Optional[int]
    end_reason: Optional[EndReason]
    created_at: datetime

    class Config:
        from_attributes = True


