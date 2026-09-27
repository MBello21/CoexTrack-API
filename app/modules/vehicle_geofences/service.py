from sqlalchemy.orm import Session
from typing import List

from .models import VehicleGeofences
from .schemas import VehicleGeofenceIn


def create_vehicle_geofence(
    db: Session,
    geofence: int,
    vehicle: int,
) -> VehicleGeofences:

    query = db.query(VehicleGeofences).filter(
        VehicleGeofences.geofence_id == geofence,
        VehicleGeofences.vehicle_id == vehicle
    ).first()

    if query:
        raise ValueError('Geofence for this vehicle already exist')

    vehicle_geofence = VehicleGeofences(
        vehicle_id=vehicle,
        geofence_id=geofence,
        alert_on_enter=True,
        alert_on_exit=True,
    )

    db.add(vehicle_geofence)
    db.flush()

    return vehicle_geofence
