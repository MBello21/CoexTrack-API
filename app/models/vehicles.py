from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from ..database import Base

if TYPE_CHECKING:
    from .device import Device


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id: Mapped[int] = mapped_column(primary_key=True)
    device: Mapped["Device"] = relationship(back_populates="vehicle")
    device_id: Mapped[str] = mapped_column(
        ForeignKey("devices.device_id"), nullable=False)
    plate: Mapped[str] = mapped_column(String(25), unique=True)
    brand: Mapped[str] = mapped_column(String(55), unique=False)
    model: Mapped[str] = mapped_column(String(55), unique=False)
    vehicle_type: Mapped[str] = mapped_column(String(55), unique=False)
    driver: Mapped[Optional[str]] = mapped_column(
        String(55), unique=False, nullable=True)
    engine_type: Mapped[str] = mapped_column(String(55), unique=False)
    last_address: Mapped[Optional[str]] = mapped_column(
        String(255), unique=False, nullable=True)
    start_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
