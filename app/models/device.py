from sqlalchemy import String, Boolean, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from datetime import datetime

from ..database import Base

if TYPE_CHECKING:
    from .telemetry import Telemetry
    from .vehicles import Vehicle


class Device(Base):
    __tablename__ = 'devices'

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column(String(25), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    vehicle: Mapped[list['Vehicle']] = relationship(
        "Vehicle",
        back_populates="device",
        cascade="all, delete-orphan"
    )
    telemetry: Mapped[list['Telemetry']] = relationship(
        "Telemetry",
        back_populates="device",
        cascade="all, delete-orphan"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
