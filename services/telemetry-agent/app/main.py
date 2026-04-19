from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlmodel import select

from entities.base import Base
from models.account import Account
from repository.account_repository import AccountRepository

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/postgres", echo=True)
Base.metadata.create_all(engine)
# with Session(engine) as session:
#     repository = AccountRepository(session)
#
#     for i in range(10):
#         repository.add_account(Account(f'Joasia_{i}'))
#
#     session.commit()
#
# with Session(engine) as session:
#     repository = AccountRepository(session)
#     account = repository.get_account_by_id(1)
#     print(account)
#
#
#
#
# with Session(engine) as session:
#     repository = AccountRepository(session)
#     repository.delete_by_id(12)
#     session.commit()


with Session(engine) as session:
    session.execute(text("TRUNCATE TABLE accounts;"))
    session.commit()



print("Finito")