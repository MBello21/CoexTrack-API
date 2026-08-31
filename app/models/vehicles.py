from sqlalchemy import String, Boolean, DateTime, Float, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geography
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from ..database import Base

if TYPE_CHECKING:
    from .telemetry import Telemetry


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[str] = mapped_column(String(25), unique=True)
    telemetry: Mapped[list['Telemetry']] = relationship(
        "Telemetry",
        back_populates="vehicle",
        cascade="all, delete-orphan"
    )
    plate: Mapped[str] = mapped_column(String(25), unique=True)
    brand: Mapped[str] = mapped_column(String(55), unique=False)
    model: Mapped[str] = mapped_column(String(55), unique=False)
    vehicle_type: Mapped[str] = mapped_column(String(55), unique=False)
    driver: Mapped[Optional[str]] = mapped_column(
        String(55), unique=False, nullable=True)
    engine_type: Mapped[str] = mapped_column(String(55), unique=False)
    last_address: Mapped[Optional[str]] = mapped_column(
        String(255), unique=False, nullable=True)
