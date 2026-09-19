from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...database import get_db
from .schemas import WorkerIn, WorkerOut
from .services import get_workers, post_worker

router = APIRouter()

@router.get("")
def get_workers_endpoint(
    skip:int = 0,
    limit: int = 8,
    db: Session = Depends(get_db) 
):
    workers = get_workers(db, skip, limit)
    return [WorkerOut.model_validate(worker) for worker in workers]

@router.post("")
def post_worker_endpoint(
    worker_data: WorkerIn, 
    db:Session = Depends(get_db),
):
    try:
        worker= post_worker(db, worker_data)
        return WorkerOut.model_validate(worker)
    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= f"Error create worker: {str(e)}"
        )