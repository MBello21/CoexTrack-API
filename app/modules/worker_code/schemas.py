from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.modules.worker.schemas import WorkerOut


class WorkerCodeIn(BaseModel):
    worker_code: str
    active: bool



class WorkerCodeOut(BaseModel):
    worker_code: str
    active: bool
    worker: Optional[list[WorkerOut]] = None
    created_at: datetime

    class Config: 
        from_attributes = True