from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from ...database import get_db

from .schemas import GeofenceIn, GeofencesOut, GeofenceUpdate
from .services import create_geofence, get_geofences, get_geofence_by_id, patch_geofence, delete_geofence


router = APIRouter()


@router.post("")
def post_geofence(
    geofence_data: GeofenceIn,
    db: Session = Depends(get_db)
):
    try:

        geofence = create_geofence(db, geofence_data)
        return GeofencesOut.model_validate(geofence)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("")
def get_geofences_endpoint(
    db: Session = Depends(get_db),
    active: bool = True
):
    geofences = get_geofences(db, active)
    return [GeofencesOut.model_validate(geofence) for geofence in geofences]


@router.get("/{geofence_id}")
def get_geofence_by_id_endpoint(
    geofence_id: int,
    db: Session = Depends(get_db),
):
    try:
        geofence = get_geofence_by_id(db, geofence_id)
        return GeofencesOut.model_validate(geofence)

    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/{geofence_id}")
def update_geofence(
    geofence_id: int,
    geofence_data: GeofenceUpdate,
    db: Session = Depends(get_db)
):
    try:
        geofence = patch_geofence(db, geofence_id, geofence_data)
        return GeofencesOut.model_validate(geofence)

    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{geofence_id}")
def delete_geofence_endpoint(
    geofence_id: int,
    db: Session = Depends(get_db)
):
    try:
        geofence = delete_geofence(db, geofence_id)
        return {'msg': 'Geofence deleted successfully'}

    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )