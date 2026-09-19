from sqlalchemy.orm import Session

from typing import List

from .models import Worker
from .schemas import WorkerIn


def get_workers(
    db: Session,
    skip: int = 0,
    limit: int = 8
) -> List[Worker]:

    query = db.query(Worker)
    return query.offset(skip).limit(limit).all()


def post_worker(
    db: Session,
    data: WorkerIn
)->Worker:

    worker = Worker(**data.model_dump())

    db.add(worker)
    db.commit()
    db.refresh(worker)

    return worker