from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely import wkt, GEOSException
from typing import List

from .models import Geofences
from .schemas import GeofenceIn, GeofenceUpdate


def create_geofence(
        db: Session,
        data: GeofenceIn
) -> Geofences:

    query = db.query(Geofences).filter(Geofences.name == data.name).first()

    if query:
        raise ValueError('Geofence already exist')

    try:
        shape = wkt.loads(data.geometry)
    except GEOSException:
        raise ValueError('Invalid poligon')

    if shape.geom_type != 'Polygon':
        raise ValueError('Geometry must be a Polygon')

    geofence = Geofences(
        name=data.name,
        geometry=from_shape(shape, srid=4326),
        geofence_type=data.geofence_type,
        active=data.active,
        description=data.description
    )

    db.add(geofence)
    db.commit()
    db.refresh(geofence)

    return geofence


def get_geofences(
    db: Session,
    active_only: bool = True
) -> List[Geofences]:

    query = db.query(Geofences)

    if active_only:
        query = query.filter(Geofences.active == True)

    return query.all()


def get_geofence_by_id(
    db: Session,
    geofence_id: int
) -> Geofences:

    geofence = db.query(Geofences).filter(Geofences.id == geofence_id).first()

    if not geofence:
        raise LookupError(f"Geofence {geofence_id} not found")
    return geofence


def patch_geofence(
    db: Session,
    geofence_id: int,
    data: GeofenceUpdate,
) -> Geofences:

    geofence = db.query(Geofences).filter(Geofences.id == geofence_id).first()

    if geofence is None:
        raise LookupError("Geofence is not found")

    if data.geometry:
        try:
            shape = wkt.loads(data.geometry)
        except GEOSException:
            raise ValueError('Invalid poligon')
        if shape.geom_type != 'Polygon':
            raise ValueError('Geometry must be a Polygon')

    for field, value in data.model_dump(exclude_unset=True).items():
        if field == 'geometry':
            geofence.geometry = from_shape(shape, srid=4326)
        else:
            setattr(geofence, field, value)

    db.commit()
    db.refresh(geofence)

    return geofence


def delete_geofence(
    db: Session,
    geofence_id: int
) -> None:

    geofence=db.query(Geofences).filter(Geofences.id == geofence_id).first()

    if geofence is None:
        raise LookupError(f"Geofence {geofence_id} not found")

    db.delete(geofence)
    db.commit()
    db.refresh()

    return
