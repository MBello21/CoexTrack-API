from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from ...database import get_db
from .schemas import UsageSessionIn, UsageSessionOut, UsageSessionEnd, UsageSessionsWithData
from .services import get_usage_session, get_usage_session_by_id, create_usage_sessions, patch_usage_session
from .enum import StatusEnum


router = APIRouter()


@router.get("")
def get_usage_session_endpoint(
    skip: int = 0,
    limit: int = 8,
    status: Optional[StatusEnum] = None,
    db: Session = Depends(get_db)
):
    usage_sessions = get_usage_session(db, skip, limit, status)
    return [UsageSessionsWithData.model_validate(usage_session) for usage_session in usage_sessions]


@router.get("/active")
def get_active_usage_session_endpoint(
    db: Session = Depends(get_db)
):
    usage_sessions = get_usage_session(db, status=StatusEnum.ACTIVE)
    return [UsageSessionsWithData.model_validate(usage_session) for usage_session in usage_sessions]


@router.get("/{usage_id}")
def get_usage_session_by_id_endpoint(
    usage_id: int,
    db: Session = Depends(get_db)
):
    usage_session = get_usage_session_by_id(db, usage_id)
    return UsageSessionsWithData.model_validate(usage_session)



@router.post("")
def create_usage_session_endpoint(
    usage_data: UsageSessionIn,
    db: Session = Depends(get_db)
):

    try:
        usage_session = create_usage_sessions(db, usage_data)
        return UsageSessionOut.model_validate(usage_session)

    except LookupError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{usage_id}", response_model=UsageSessionOut)
def patch_usage_sessions_endpoint(
    usage_id: int,
    usage_data: UsageSessionEnd,
    db: Session = Depends(get_db)
):
    try:
        usage_session = patch_usage_session(usage_id, db, usage_data)
        return UsageSessionOut.model_validate(usage_session)

    except LookupError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
