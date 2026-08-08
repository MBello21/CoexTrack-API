from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement
from ..schemas import TelemetryIn
from ..models import Telemetry
from ..database import get_db

router = APIRouter()


@router.post("")
def create_telemetry(data: TelemetryIn, db: Session = Depends(get_db)):
    telemetry = Telemetry(
        vehicle_id=data.vehicle_id,
        timestamp=data.timestamp,
        location=WKTElement(f"POINT({data.lon} {data.lat})", srid=4326),
        alt=data.alt,
        speed=data.speed,
        course=data.course,
        sats=data.sats,
        hdop=data.hdop,
        ignition=data.ignition,
    )
    db.add(telemetry)
    db.commit()
    return {"status": "ok"}
