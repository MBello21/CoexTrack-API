from pydantic import BaseModel
from pydantic import model_validator

from typing import Optional


class GeofenceIn(BaseModel):
    name: str
    geometry: str
    geofence_type: str
    active: bool = True
    description: Optional[str]


class GeofencesOut(BaseModel):
    id: int
    name: str
    geometry: str
    geofence_type: str
    active: bool
    description: Optional[str]

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    @classmethod
    def convert_geometry(cls, data):
        if hasattr(data, "geometry") and data.geometry:
            from geoalchemy2.shape import to_shape
            data.geometry = to_shape(data.geometry).wkt
        return data
