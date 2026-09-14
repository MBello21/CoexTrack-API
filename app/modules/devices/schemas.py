from pydantic import BaseModel


class DeviceIn(BaseModel):
    device_id: str


class DeviceOut(BaseModel):
    id: int
    device_id: str
    active: bool

    class Config:
        from_attributes = True
