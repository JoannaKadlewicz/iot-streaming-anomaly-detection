from sqlalchemy import select
from sqlalchemy.orm import Session

from entities.account import AccountEntity
from models.account import Account


class AccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_account_by_id(self, account_id: int) -> Account | None:
        account_entity = self.session.get(AccountEntity, account_id)
        return self._from_entity(account_entity)

    def get_account_by_name(self, name: str) -> Account | None:
        statement = select(AccountEntity).where(AccountEntity.name == name)
        account_entity = self.session.execute(statement).first()
        return self._from_entity(account_entity)

    def add_account(self, account: Account) -> None:
        account_entity = AccountEntity(name=account.name, created_at=account.created_at, is_active=account.is_active)
        self.session.add(account_entity)

    def delete_by_id(self, account_id: int) -> None:
        account_to_delete = self.session.get(AccountEntity, account_id)
        self.session.delete(account_to_delete)

    def _from_entity(self, account_entity: AccountEntity) -> Account:
        return Account(name=account_entity.name, created_at=account_entity.created_at,
                       is_active=account_entity.is_active)
