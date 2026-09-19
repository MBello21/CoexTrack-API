from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...database import get_db
from .schemas import WorkerCodeIn, WorkerCodeOut
from .services import get_worker_code, post_worker_code


router = APIRouter()


@router.get("")
def get_worker_code_endpoint(
    skip: int = 0,
    limit: int = 8,
    db: Session = Depends(get_db)
):

    workers_codes = get_worker_code(db, skip, limit)
    return [WorkerCodeOut.model_validate(worker_code) for worker_code in workers_codes]


@router.post("")
def post_worker_code_endpoint(
    worker_code_data: WorkerCodeIn,
    db: Session = Depends(get_db)
):
    try:
        worker_code = post_worker_code(db, worker_code_data)
        return WorkerCodeOut.model_validate(worker_code)

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error create worker code: {str(e)}"
        )
