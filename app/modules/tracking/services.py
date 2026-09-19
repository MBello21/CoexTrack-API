from sqlalchemy.orm import Session, joinedload
from geoalchemy2.elements import WKTElement
from sqlalchemy import func

from typing import List
from datetime import datetime

from .models import Telemetry
from app.modules.usage_sessions.models import UsageSessions
from app.modules.devices.models import Device

from .schemas import TelemetryIn

from app.modules.usage_sessions.enum import StatusEnum


def get_latest_telemetry(
    db: Session
) -> List[Telemetry]:

    subquery = db.query(
        func.max(Telemetry.id)
    ).join(
        Device, Telemetry.device_id == Device.device_id
    ).filter(
        Device.active == True
    ).group_by(
        Telemetry.device_id
    ).subquery()

    queries = db.query(Telemetry).filter(
        Telemetry.id.in_(subquery)
    ).options(
        joinedload(Telemetry.device).joinedload(Device.vehicle),
        joinedload(Telemetry.session).joinedload(UsageSessions.worker)
    ).all()

    return queries


def get_history_telemetry(
    db: Session,
    start: datetime,
    end: datetime,
    device_id: str,
) -> List[Telemetry]:
    queries = db.query(Telemetry).filter(
        Telemetry.device_id == device_id,
        Telemetry.timestamp.between(start, end)
    ).options(
        joinedload(Telemetry.device).joinedload(Device.vehicle),
        joinedload(Telemetry.session).joinedload(UsageSessions.worker)
    ).order_by(Telemetry.timestamp.asc()).all()

    return queries


def post_telemetry(
    db: Session,
    data: TelemetryIn,
) -> None:

    if not data.session_id:
        active = db.query(UsageSessions).filter(
            UsageSessions.device_id == data.device_id,
            UsageSessions.status == StatusEnum.ACTIVE
        ).first()

        session_id = active.id if active else None
    else:
        session_id = data.session_id
    telemetry = Telemetry(
        device_id=data.device_id,
        session_id=session_id,
        timestamp=data.timestamp,
        location=WKTElement(f"POINT({data.lon} {data.lat})", srid=4326),
        alt=data.alt,
        speed=data.speed,
        course=data.course,
        sats=data.sats,
        hdop=data.hdop,
        ignition=data.ignition,
        aspa_active=data.aspa_active,
        battery_voltage=data.battery_voltage,
        battery_current_ma=data.battery_current_ma,
        alert=data.alert,
    )

    db.add(telemetry)
    db.commit()

    return


def post_batch_telemetry(
    db: Session,
    data: List[TelemetryIn],

) -> None:

    active_sessions = db.query(UsageSessions).filter(
        UsageSessions.status == StatusEnum.ACTIVE
    ).all()

    session_map = {s.device_id: s.id for s in active_sessions}

    for d in data:
        telemetry = Telemetry(
            device_id=d.device_id,
            session_id=d.session_id or session_map.get(d.device_id),
            timestamp=d.timestamp,
            location=WKTElement(f"POINT({d.lon} {d.lat})", srid=4326),
            alt=d.alt,
            speed=d.speed,
            course=d.course,
            sats=d.sats,
            hdop=d.hdop,
            ignition=d.ignition,
            aspa_active=d.aspa_active,
            battery_voltage=d.battery_voltage,
            battery_current_ma=d.battery_current_ma,
            alert=d.alert,
        )
        db.add(telemetry)
    db.commit()

    return
