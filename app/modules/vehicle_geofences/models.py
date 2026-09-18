from sqlalchemy import ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from ...database import Base


if TYPE_CHECKING:
    from app.modules.vehicles.models import Vehicle
    from app.modules.geofences.models import Geofences


class VehicleGeofences (Base):

    __tablename__ = 'vehicle_geofences'

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle: Mapped["Vehicle"] = relationship(
        back_populates="vehicle_geofences")
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"), nullable=False)
    geofence: Mapped["Geofences"] = relationship(
        back_populates="vehicle_geofences")
    geofence_id: Mapped[int] = mapped_column(
        ForeignKey("geofences.id"), nullable=False)
    alert_on_enter: Mapped[bool] = mapped_column(Boolean)
    alert_on_exit: Mapped[bool] = mapped_column(Boolean)

    __table_args__ = (
                        UniqueConstraint("vehicle_id", "geofence_id", name="uq_vehicle_geofence"),
                    )
