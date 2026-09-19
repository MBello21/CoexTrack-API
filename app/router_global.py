from fastapi import APIRouter
from app.modules.tracking.router import router as telemetry_router
from app.modules.vehicles.router import router as vehicle_router
from app.modules.devices.router import router as device_router
from app.modules.usage_sessions.router import router as usage_session_router

api_router = APIRouter()

api_router.include_router(
    telemetry_router, prefix="/telemetry", tags=["telemetry"])
api_router.include_router(vehicle_router, prefix="/vehicle", tags=["vehicle"])
api_router.include_router(device_router, prefix="/device", tags=["device"])
api_router.include_router(usage_session_router, prefix="/usage-session", tags=["usage-session"])
