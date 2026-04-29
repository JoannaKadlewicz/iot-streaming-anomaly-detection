import json
from datetime import datetime, UTC
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from domain.entities.account import Account
from domain.entities.device import Device, DeviceType, Capability
from infrastructure.persistence.models.base import BaseModel
from infrastructure.persistence.repository.account_repository import AccountRepository
from infrastructure.persistence.repository.device_repository import DeviceRepository

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures/samples"


def load_json(filename: str) -> list[dict]:
    path = FIXTURES_DIR / filename
    return json.loads(path.read_text(encoding="utf-8"))


def drop_and_recreate_tables(engine) -> None:
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
    print("Tables created: ['accounts', 'devices']")


def seed_accounts(session: Session) -> dict[str, int]:
    repo = AccountRepository(session)
    data = load_json("accounts.json")
    account_map = {}

    for item in data:
        account = Account(account_id=None, name=item["name"], is_active=item["is_active"])
        repo.add_account(account)
        session.flush()

        saved = repo.get_account_by_name(account.name)
        account_map[account.name] = saved.account_id
        print(f"  + Account: {account.name} (id={saved.account_id})")

    return account_map


def seed_devices(session: Session, account_map: dict[str, int]) -> None:
    repo = DeviceRepository(session)
    data = load_json("devices.json")

    for item in data:
        device = Device(
            device_id=None,
            name=item["name"],
            account_id=account_map[item["account_name"]],
            device_type=DeviceType(item["device_type"]),
            capabilities=[Capability(c) for c in item["capabilities"]],
            created_at=datetime.now(UTC),
        )
        repo.add_device(device)
        print(f"  + Device: {device.name} [{item['name']}] → [{item['device_type']}]")


def load_samples(settings):
    engine = create_engine(settings.postgres_dsn, echo=False)

    print("Creating tables...")
    drop_and_recreate_tables(engine)

    print("\n Seeding...")
    with Session(engine) as session:
        account_map = seed_accounts(session)
        print()
        seed_devices(session, account_map)
        session.commit()
        print(f"\n Seed finished.")
