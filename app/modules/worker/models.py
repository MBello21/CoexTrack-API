from sqlalchemy import String, ForeignKey, Date,Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from ...database import Base

if TYPE_CHECKING:
    from app.modules.worker_code.models import WorkerCode
    from app.modules.usage_sessions.models import UsageSessions


class Worker(Base):
    __tablename__ = 'workers'

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(55), unique=False)
    last_name: Mapped[str] = mapped_column(String(55), unique=False)
    phone: Mapped[Optional[str]] = mapped_column(
        String(25), unique=True, nullable=True)
    dni: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    worker_code: Mapped["WorkerCode"] = relationship(back_populates="worker")
    worker_code_id: Mapped[str] = mapped_column(
            ForeignKey("worker_code.worker_code"), nullable=False)
    usage_session: Mapped[list['UsageSessions']] = relationship(
                    "UsageSessions",
                    back_populates="worker",
                )
    start_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)

    __table_args__ = (
                Index(
                    "uq_one_active_worker_per_worker_code",
                    "worker_code_id",
                    unique=True,
                    postgresql_where=(end_date.is_(None))
                ),
            )