from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import text
from geoalchemy2.elements import WKTElement
from datetime import datetime
from ..schemas import TelemetryIn, TelemetryOut
from ..models import Telemetry
from ..database import get_db
from typing import List

router = APIRouter()

# Gestión simple de conexiones
class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.remove(ws)

    async def broadcast(self, data: dict):
        for ws in self.connections:
            try:
                await ws.send_json(data)
            except:
                self.connections.remove(ws)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()  # mantiene la conexión viva
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
    )
    db.add(telemetry)
    db.commit()

    # Notifica a todos los frontends
    await manager.broadcast(data.model_dump())

    return {"status": "ok"}


@router.get("/latest", response_model=list[TelemetryOut])
def get_latest_positions(db: Session = Depends(get_db)):
    """Última posición de cada vehículo."""
    sql = text("""
        SELECT DISTINCT ON (vehicle_id)
            vehicle_id, timestamp,
            ST_Y(location::geometry) AS lat,
            ST_X(location::geometry) AS lon,
            alt, speed, course, sats, hdop, ignition
        FROM telemetry
        ORDER BY vehicle_id, timestamp DESC
    """)
    rows = db.execute(sql).mappings().all()
    return [dict(r) for r in rows]


@router.get("/history/{vehicle_id}", response_model=list[TelemetryOut])
def get_vehicle_history(
    vehicle_id: str,
    start: datetime = Query(..., description="Inicio del rango"),
    end: datetime = Query(..., description="Fin del rango"),
    db: Session = Depends(get_db),
):
    """Historial de posiciones de un vehículo en un rango de tiempo."""
    sql = text("""
        SELECT
            vehicle_id, timestamp,
            ST_Y(location::geometry) AS lat,
            ST_X(location::geometry) AS lon,
            alt, speed, course, sats, hdop, ignition
        FROM telemetry
        WHERE vehicle_id = :vid
          AND timestamp BETWEEN :start AND :end
        ORDER BY timestamp ASC
    """)
    rows = db.execute(sql, {"vid": vehicle_id, "start": start, "end": end}).mappings().all()
    return [dict(r) for r in rows]