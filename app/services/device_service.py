from sqlalchemy.orm import Session

from typing import List

from ..models.device import Device
from ..schemas.device import DeviceIn, DeviceOut


def get_device(
    db: Session,
    skip: int = 0,
    limit: int = 10,
) -> List[Device]:

    query = db.query(Device)
    return query.offset(skip).limit(limit).all()


def create_device(
    db: Session,
    data: DeviceIn
) -> Device:

    device = Device(**data.model_dump())

    db.add(device)
    db.commit()
    db.refresh(device)
    return device
