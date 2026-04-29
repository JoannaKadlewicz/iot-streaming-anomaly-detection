from dataclasses import dataclass
from datetime import datetime

from infrastructure.persistence.models.device import DeviceType, Capability


@dataclass
class Device:
    name: str
    account_id: int
    device_type: DeviceType
    capabilities: list[Capability]
    created_at: datetime
