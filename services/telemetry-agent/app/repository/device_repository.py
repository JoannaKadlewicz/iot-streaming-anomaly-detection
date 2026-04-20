from sqlalchemy.orm import Session
from sqlalchemy import select
from entities.account import AccountEntity
from entities.device import DeviceEntity
from models.device import Device
from repository.account_repository import AccountRepository


class DeviceRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_device_by_id(self, device_id: int) -> Device:
        device_entity = self.session.get(DeviceEntity, device_id)
        return self._from_entity(device_entity)

    def get_devices_by_account_id(self, account_id: int) -> list[Device]:
        query = select(DeviceEntity).where(DeviceEntity.account_id == account_id)
        device_entities = self.session.execute(query).scalars().all()

        list_of_devices = []
        for device in device_entities:
            list_of_devices.append(self._from_entity(device))
        return list_of_devices

        # return [_from_entity(device_entity) for device_entity in device_entities]


    def _from_entity(self, device_entity: DeviceEntity) -> Device:
        return Device(name=device_entity.name, device_type=device_entity.device_type,
                      capabilities=device_entity.capabilities)
