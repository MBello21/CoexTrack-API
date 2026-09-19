from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect, BackgroundTasks
from sqlalchemy.orm import Session

from datetime import datetime
from typing import List
from .schemas import TelemetryIn, TelemetryWithDataOut

from .services import get_latest_telemetry, get_history_telemetry, post_telemetry, post_batch_telemetry
from ...database import get_db
from app.shared.geocode import update_vehicle_address



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


@router.get("/latest", response_model=list[TelemetryWithDataOut])
def get_latest_positions(db: Session = Depends(get_db)):

    latests = get_latest_telemetry(db)
    return [TelemetryWithDataOut.model_validate(latest) for latest in latests]


@router.get("/history/{device_id}", response_model=list[TelemetryWithDataOut])
def get_vehicle_history(
    device_id: str,
    start: datetime = Query(..., description="Inicio del rango"),
    end: datetime = Query(..., description="Fin del rango"),
    db: Session = Depends(get_db),
):

    histories = get_history_telemetry(db, start, end, device_id)

    return [TelemetryWithDataOut.model_validate(history) for history in histories]


@router.post("")
async def create_telemetry(
        telemetry_data: TelemetryIn,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),

):
    post_telemetry(db, telemetry_data)
    await manager.broadcast(telemetry_data.model_dump(mode='json'))
    background_tasks.add_task(update_vehicle_address,
                              telemetry_data.device_id, telemetry_data.lat, telemetry_data.lon)

    return {"status": "ok"}


@router.post("/batch")
async def create_telemetry_batch(
    telemetry_data: List[TelemetryIn],
    db: Session = Depends(get_db)
):

    post_batch_telemetry(db, telemetry_data)
    
    await manager.broadcast(telemetry_data[-1].model_dump(mode='json'))
    return {"status": "ok", "count": len(telemetry_data)}
