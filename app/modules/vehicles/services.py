from sqlalchemy.orm import Session

from typing import List

from .models import Vehicle
from .schemas import VehicleIn


def get_vehicle(
    db: Session,
    skip: int = 0,
    limit: int = 10,
) -> List[Vehicle]:

    query = db.query(Vehicle)
    return query.offset(skip).limit(limit).all()


def create_vehicle(
    db: Session,
    data: VehicleIn
) -> Vehicle:

    vehicle = Vehicle(**data.model_dump())

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle
