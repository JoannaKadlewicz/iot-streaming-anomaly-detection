from dataclasses import dataclass

from entities.device import DeviceType, Capability, DeviceEntity


@dataclass
class Device:
    name: str
    device_type: DeviceType
    capabilities: list[Capability]