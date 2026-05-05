import json

from domain.model import Device


def fetch_devices(file_source: str) -> list[Device]:
    with open(file_source) as f:
        devices = json.load(f)
        return [Device(**device) for device in devices]
