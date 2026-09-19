from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WorkerIn(BaseModel):
    category: str
    name: str
    last_name: str
    phone: Optional[str] = None
    dni: str
    worker_code_id: str
    start_date: datetime


class WorkerOut(BaseModel):
    id: int
    category: str
    name: str
    last_name: str
    phone: Optional[str] = None
    dni: str
    worker_code_id: str
    start_date: datetime

    class Config:
        from_attributes = True
