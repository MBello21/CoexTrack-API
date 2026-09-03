from sqlalchemy import String, Boolean, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geography
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from ..database import Base

if TYPE_CHECKING:
    from .device import Device


class Telemetry(Base):
    __tablename__ = 'telemetry'

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column(
        ForeignKey("devices.device_id"), nullable=True)
    device: Mapped["Device"] = relationship(
        "Device",
        back_populates='telemetry'
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False)
    location: Mapped[str] = mapped_column(
        Geography(geometry_type='POINT', srid=4326), nullable=False)
    alt: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    speed: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    course: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sats: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    hdop: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ignition: Mapped[bool] = mapped_column(Boolean, default=False)
    aspa_active: Mapped[bool] = mapped_column(Boolean, default=False)
    battery_voltage: Mapped[Optional[float]
                            ] = mapped_column(Float, nullable=True)
    battery_current_ma: Mapped[Optional[float]
                               ] = mapped_column(Float, nullable=True)
    alert: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
