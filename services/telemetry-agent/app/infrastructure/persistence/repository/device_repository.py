from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities import Device
from infrastructure.persistence.models import DeviceModel


class DeviceRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_device_by_id(self, device_id: int) -> Device:
        device_model = self.session.get(DeviceModel, device_id)
        if device_model is None:
            raise ValueError(f"Device with id={device_id} not found")
        return self._from_model(device_model)

    def get_devices_by_account_id(self, account_id: int) -> list[Device]:
        query = select(DeviceModel).where(DeviceModel.account_id == account_id)
        device_models = self.session.execute(query).scalars().all()

        list_of_devices = []
        for device in device_models:
            list_of_devices.append(self._from_model(device))
        return list_of_devices

    def add_device(self, device: Device) -> None:
        model = DeviceModel(
            name=device.name,
            account_id=device.account_id,
            device_type=device.device_type,
            capabilities=device.capabilities,
            created_at=device.created_at,
        )
        self.session.add(model)

    def _from_model(self, device_model: DeviceModel) -> Device:
        return Device(name=device_model.name, account_id=device_model.account_id,
                      device_type=device_model.device_type,
                      capabilities=device_model.capabilities,
                      created_at=device_model.created_at)
