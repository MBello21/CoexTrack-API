from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.vehicles import Vehicle
from ..schemas.vehicles import VehicleIn, VehicleOut
from ..services.vehicles_service import (create_vehicle, get_vehicle)

router = APIRouter()


@router.get("")
def get_vehicle_endpoint(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    vehicles = get_vehicle(db, skip, limit)
    return [VehicleOut.model_validate(vehicle) for vehicle in vehicles]


@router.post("")
def create_vehicle_endpoint(
    vehicle_data: VehicleIn,
    db: Session = Depends(get_db)
):
    try:
        vehicle = create_vehicle(db, vehicle_data)
        return VehicleOut.model_validate(vehicle)
    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error create vehicle: {str(e)}"
        )
