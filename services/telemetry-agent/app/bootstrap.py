from sqlalchemy.orm import Session

from domain.entities import Device
from infrastructure.persistence.repository.account_repository import AccountRepository
from infrastructure.persistence.repository.device_repository import DeviceRepository


def ensure_seeded(engine, settings) -> None:
    with Session(engine) as session:
        repo = AccountRepository(session)
        if not repo.has_accounts():
            from seed.seed import load_samples
            load_samples(settings)


def fetch_devices(engine, account_id: int) -> list[Device]:
    with Session(engine) as session:
        repo = DeviceRepository(session)
        return repo.get_devices_by_account_id(account_id)
