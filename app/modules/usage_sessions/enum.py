from enum import Enum


class StatusEnum(Enum):
    ACTIVE = 'active'
    FINISHED = 'finished'


class EndReason(Enum):
    GEOFENCE = 'geofence'
    MANUAL = 'manual'
    TIMEOUT = 'timeout'
