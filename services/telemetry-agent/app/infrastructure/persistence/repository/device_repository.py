from sqlalchemy.orm import Session
from sqlalchemy import select
from infrastructure.persistence.models import DeviceModel
from domain.entities import Device


class DeviceRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_device_by_id(self, device_id: int) -> Device:
        device_entity = self.session.get(DeviceModel, device_id)
        return self._from_entity(device_entity)

    def get_devices_by_account_id(self, account_id: int) -> list[Device]:
        query = select(DeviceModel).where(DeviceModel.account_id == account_id)
        device_entities = self.session.execute(query).scalars().all()

        list_of_devices = []
        for device in device_entities:
            list_of_devices.append(self._from_entity(device))
        return list_of_devices

        # return [_from_entity(device_entity) for device_entity in device_entities]


    def _from_entity(self, device_entity: DeviceModel) -> Device:
        return Device(name=device_entity.name, device_type=device_entity.device_type,
                      capabilities=device_entity.capabilities)
