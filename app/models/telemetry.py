from sqlalchemy import String, Boolean, DateTime, Float, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from geoalchemy2 import Geography
from datetime import datetime
from typing import Optional
from ..database import Base


class Telemetry(Base):
    __tablename__ = 'telemetry'

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[str] = mapped_column(
        # no unique, un vehículo manda muchos registros
        String(20), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False)
    location: Mapped[str] = mapped_column(
        Geography(geometry_type='POINT', srid=4326), nullable=False)
    alt: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    speed: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    course: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sats: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    hdop: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ignition: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
