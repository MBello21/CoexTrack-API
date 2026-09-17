from sqlalchemy import String, Boolean, func, DateTime, ForeignKey, Enum, Float, Text, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geography
from typing import TYPE_CHECKING
from datetime import datetime

from ...database import Base
from .enum import StatusEnum, EndReason

if TYPE_CHECKING:
    from app.modules.worker.models import Worker
    from app.modules.devices.models import Device
    from app.modules.vehicles.models import Vehicle
    from app.modules.tracking.models import Telemetry


class UsageSessions(Base):
    __tablename__ = 'usage_sessions'

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle: Mapped["Vehicle"] = relationship(back_populates="usage_session")
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"), nullable=False)
    worker: Mapped["Worker"] = relationship(back_populates="usage_session")
    worker_id: Mapped[int] = mapped_column(
        ForeignKey("workers.id"), nullable=False)
    device: Mapped["Device"] = relationship(back_populates="usage_session")
    device_id: Mapped[str] = mapped_column(
        ForeignKey("devices.device_id"), nullable=False)
    telemetry: Mapped[list['Telemetry']] = relationship(
        "Telemetry",
        back_populates="session",
    )
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum), nullable=False, default=StatusEnum.ACTIVE)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    start_odometer: Mapped[float] = mapped_column(Float, nullable=False)
    start_location: Mapped[str] = mapped_column(
        Geography(geometry_type='POINT', srid=4326), nullable=False)
    trip_purpose: Mapped[str] = mapped_column(String(500), nullable=True)
    pre_check_notes: Mapped[str] = mapped_column(Text, nullable=True)
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True)
    end_odometer: Mapped[float] = mapped_column(Float, nullable=True)
    end_location: Mapped[str] = mapped_column(
        Geography(geometry_type='POINT', srid=4326), nullable=True)
    total_km: Mapped[float] = mapped_column(Float, nullable=True)
    total_seconds:Mapped[int]=mapped_column(Integer, nullable=True)
    end_reason: Mapped[EndReason] = mapped_column(Enum(EndReason), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
                    Index(
                        "uq_one_active_sesion_per_vehicle_id",
                        "vehicle_id",
                        unique=True,
                        postgresql_where=(status == StatusEnum.ACTIVE)
                    ),
                )