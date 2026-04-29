from sqlalchemy import select, inspect, func
from sqlalchemy.orm import Session

from domain.entities import Account
from infrastructure.persistence.models import AccountModel


class AccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_account_by_id(self, account_id: int) -> Account:
        account_model = self.session.get(AccountModel, account_id)
        if account_model is None:
            raise ValueError(f"Account with id={account_id} not found")
        return self._from_model(account_model)

    def get_account_by_name(self, name: str) -> Account:
        statement = select(AccountModel).where(AccountModel.name == name)
        account_model = self.session.execute(statement).scalar_one_or_none()
        if account_model is None:
            raise ValueError(f"Account with name={name} not found")
        return self._from_model(account_model)

    def add_account(self, account: Account) -> None:
        account_model = AccountModel(name=account.name, created_at=account.created_at, is_active=account.is_active)
        self.session.add(account_model)

    def delete_by_id(self, account_id: int) -> None:
        account_to_delete = self.session.get(AccountModel, account_id)
        self.session.delete(account_to_delete)

    def table_exists(self) -> bool:
        inspector = inspect(self.session.bind)
        return inspector.has_table("accounts")

    def has_accounts(self) -> bool:
        if not self.table_exists():
            return False
        count = self.session.execute(
            select(func.count()).select_from(AccountModel)
        ).scalar()
        return count > 0

    def _from_model(self, account_model: AccountModel) -> Account:
        return Account(name=account_model.name, account_id=account_model.account_id,
                       created_at=account_model.created_at,
                       is_active=account_model.is_active)
