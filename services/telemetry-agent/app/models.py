from sqlalchemy import Column, String, BigInteger
from sqlmodel import SQLModel, Field


class Account(SQLModel, table=True):
    __tablename__ = "accounts"
    __table_args__ = {"schema": "sensors"}

    id: int | None = Field(sa_column= Column(BigInteger, primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column(String(100), nullable=False, name="account_name"))
