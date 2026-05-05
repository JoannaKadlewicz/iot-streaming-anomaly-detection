from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class DeviceType(str, Enum):
    WATCH = "smartwatch"
    BAND = "smart band"
    RING = "smart ring"


class Capability(str, Enum):
    STEPS = "steps"
    TEMPERATURE = "temperature"
    HEART_RATE = "heart_rate"
    BLOOD_PRESSURE = "blood_pressure"


@dataclass
class Device:
    device_id: int
    name: str
    account_id: int
    device_type: DeviceType
    capabilities: list[Capability]
    created_at: datetime