from fastapi import APIRouter
from .router.telemetry import router as telemetry_router
from .router.vehicles import router as vehicle_router

api_router = APIRouter()

api_router.include_router(
    telemetry_router, prefix="/telemetry", tags=["telemetry"])
api_router.include_router(vehicle_router, prefix="/vehicle", tags=["vehicle"])
