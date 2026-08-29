from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import text
from geoalchemy2.elements import WKTElement
from datetime import datetime
from typing import List
from ..schemas import TelemetryIn, TelemetryOut, TelemetryWithVehicleOut
from ..models import Telemetry
from ..database import get_db


router = APIRouter()


class ConecctionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.remove(ws)

    async def broadcast(self, data: dict):
        dead = []
        for ws in self.connections:
            try:
                await ws.send_json(data)
            except:
                dead.append(ws)
        for ws in dead:
            self.connections.remove(ws)


manager = ConecctionManager()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)

    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)


@router.post("")
async def create_telemetry(data: TelemetryIn, db: Session = Depends(get_db)):
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
        aspa_active=data.aspa_active,
        battery_voltage=data.battery_voltage,
        battery_current_ma=data.battery_current_ma,
        alert=data.alert,
    )

    db.add(telemetry)
    db.commit()

    await manager.broadcast(data.model_dump(mode='json'))
    return {"status": "ok"}


@router.get("/latest", response_model=list[TelemetryWithVehicleOut])
def get_latest_positions(db: Session = Depends(get_db)):
    """Última posición de cada vehículo."""
    sql = text("""
        SELECT DISTINCT ON (telemetry.vehicle_id)
            telemetry.vehicle_id, timestamp,
            ST_Y(location::geometry) AS lat,
            ST_X(location::geometry) AS lon,
            alt, speed, course, sats, hdop, ignition,
            aspa_active, battery_voltage, battery_current_ma, alert,vehicles.plate, 
            vehicles.brand, vehicles.model, vehicles.vehicle_type, vehicles.driver, vehicles.engine_type
        FROM telemetry
        LEFT JOIN vehicles ON telemetry.vehicle_id = vehicles.vehicle_id
        ORDER BY telemetry.vehicle_id, timestamp DESC
    """)
    rows = db.execute(sql).mappings().all()
    return [dict(r) for r in rows]


@router.get("/history/{vehicle_id}", response_model=list[TelemetryWithVehicleOut])
def get_vehicle_history(
    vehicle_id: str,
    start: datetime = Query(..., description="Inicio del rango"),
    end: datetime = Query(..., description="Fin del rango"),
    db: Session = Depends(get_db),
):
    """Historial de posiciones de un vehículo en un rango de tiempo."""
    sql = text("""
        SELECT
            telemetry.vehicle_id, timestamp,
            ST_Y(location::geometry) AS lat,
            ST_X(location::geometry) AS lon,
            alt, speed, course, sats, hdop, ignition,
            aspa_active, battery_voltage, battery_current_ma, alert,vehicles.plate, 
            vehicles.brand, vehicles.model, vehicles.vehicle_type, vehicles.driver, vehicles.engine_type
        FROM telemetry
        LEFT JOIN vehicles ON telemetry.vehicle_id = vehicles.vehicle_id
        WHERE telemetry.vehicle_id = :vid
          AND timestamp BETWEEN :start AND :end
        ORDER BY timestamp ASC
    """)
    rows = db.execute(
        sql, {"vid": vehicle_id, "start": start, "end": end}).mappings().all()
    return [dict(r) for r in rows]


@router.post("/batch")
async def create_telemetry_batch(data: List[TelemetryIn], db: Session = Depends(get_db)):
    for d in data:
        telemetry = Telemetry(
            vehicle_id=d.vehicle_id,
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
    await manager.broadcast(data[-1].model_dump(mode='json'))
    return {"status": "ok", "count": len(data)}
