from sqlalchemy import String, Boolean, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from ...database import Base

if TYPE_CHECKING: 
    from app.modules.vehicle_geofences.models import VehicleGeofences


class Geofences(Base):
    __tablename__ = 'geofences'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    geometry: Mapped[str] = mapped_column(
        Geometry(geometry_type='POLYGON', srid=4326), nullable=False)
    geofence_type: Mapped[str] = mapped_column(String(120), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    vehicle_geofences: Mapped[list['VehicleGeofences']] = relationship(
        "VehicleGeofences",
        back_populates="geofence",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
