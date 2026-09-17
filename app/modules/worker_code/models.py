from sqlalchemy import String, Boolean, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from datetime import datetime

from ...database import Base

if TYPE_CHECKING:
    from app.modules.worker.models import Worker


class WorkerCode(Base):
    __tablename__ = 'worker_code'

    id: Mapped[int] = mapped_column(primary_key=True)
    worker_code: Mapped[str] = mapped_column(String(25), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    worker: Mapped[list['Worker']] = relationship(
        "Worker",
        back_populates="worker_code",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

   