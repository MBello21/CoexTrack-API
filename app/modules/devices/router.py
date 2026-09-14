from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...database import get_db
from .models import Device
from .schemas import DeviceIn, DeviceOut
from .services import get_device, create_device

router = APIRouter()


@router.get("")
def get_device_endpoint(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    devices = get_device(db, skip, limit)
    return [DeviceOut.model_validate(device) for device in devices]


@router.post("")
def create_device_endpoint(
    device_data: DeviceIn,
    db: Session = Depends(get_db)
):
    try:
        device = create_device(db, device_data)
        return DeviceOut.model_validate(device)
    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error create device: {str(e)}"
        )
