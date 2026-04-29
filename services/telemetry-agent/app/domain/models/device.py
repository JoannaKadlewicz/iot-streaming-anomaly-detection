from dataclasses import dataclass

from infrastructure.persistence.entities.device import DeviceType, Capability


@dataclass
class Device:
    name: str
    device_type: DeviceType
    capabilities: list[Capability]