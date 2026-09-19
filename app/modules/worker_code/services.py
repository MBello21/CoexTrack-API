from sqlalchemy.orm import Session

from typing import List

from .models import WorkerCode
from .schemas import WorkerCodeIn


def get_worker_code(
    db: Session,
    skip: int = 0,
    limit: int = 8
) -> List[WorkerCode]:

    query = db.query(WorkerCode)
    return query.offset(skip).limit(limit).all()

def post_worker_code(
    db: Session,
    data: WorkerCodeIn
) -> WorkerCode:

    worker_code = WorkerCode(**data.model_dump())

    db.add(worker_code)
    db.commit()
    db.refresh(worker_code)

    return worker_code