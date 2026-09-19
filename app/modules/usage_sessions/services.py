from sqlalchemy.orm import Session, joinedload
from typing import Optional
from datetime import datetime, timezone

from typing import List

from .models import UsageSessions
from .schemas import UsageSessionIn, UsageSessionEnd
from .enum import StatusEnum


from app.modules.vehicles.models import Vehicle
from app.modules.worker.models import Worker


def get_usage_session(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    status: Optional[StatusEnum] = None

) -> List[UsageSessions]:
    query = db.query(UsageSessions).options(
        joinedload(UsageSessions.vehicle),
        joinedload(UsageSessions.worker)
    )

    if status is not None:
        query = query.filter(UsageSessions.status == status)

    return query.order_by(UsageSessions.start_time.desc()).offset(skip).limit(limit).all()


def get_usage_session_by_id(
    db: Session,
    usage_id: int
) -> UsageSessions:
    query = db.query(UsageSessions).filter(UsageSessions.id == usage_id).options(
        joinedload(UsageSessions.vehicle),
        joinedload(UsageSessions.worker)
    ).first()

    if query is None:
        raise LookupError("Session not found")

    return query

def create_usage_sessions(
    db: Session,
    data: UsageSessionIn
) -> UsageSessions:

    vehicle = db.query(Vehicle).filter(Vehicle.id == data.vehicle_id).first()
    if vehicle is None:
        raise LookupError("Vehicle not found")

    worker = db.query(Worker).filter(Worker.id == data.worker_id).first()
    if worker is None:
        raise LookupError("Worker not found")

    if vehicle.end_date is not None:
        raise ValueError("Vehicle is not active")

    if worker.end_date is not None:
        raise ValueError("Worker is not active")

    active_session = db.query(UsageSessions).filter(
        UsageSessions.vehicle_id == data.vehicle_id,
        UsageSessions.status == StatusEnum.ACTIVE
    ).first()
    if active_session is not None:
        raise ValueError("The vehicle has an active session")

    usage_session = UsageSessions(**data.model_dump())
    usage_session.device_id = vehicle.device_id

    db.add(usage_session)
    db.commit()
    db.refresh(usage_session)

    return usage_session


def patch_usage_session(
        usage_id: int,
        db: Session,
        data: UsageSessionEnd,
) -> UsageSessions:

    usage_session = db.query(UsageSessions).filter(
        UsageSessions.id == usage_id).first()

    if usage_session is None:
        raise LookupError("Session is not found")

    if usage_session.status != StatusEnum.ACTIVE:
        raise ValueError("The vehicle has an active session")

    usage_session.end_time = datetime.now(timezone.utc)
    usage_session.end_odometer = data.end_odometer
    usage_session.end_location = data.end_location
    usage_session.end_reason = data.end_reason
    usage_session.total_km = data.end_odometer - usage_session.start_odometer
    usage_session.total_seconds = int(
        (usage_session.end_time - usage_session.start_time).total_seconds())
    usage_session.status = StatusEnum.FINISHED

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == usage_session.vehicle_id).first()
    vehicle.odometer = data.end_odometer

    db.commit()
    db.refresh(usage_session)

    return usage_session
