from pydantic_settings import BaseSettings


class Config(BaseSettings):
    postgres_dsn: str
    kafka_bootstrap_servers: str
    account_id: int
    debug: bool = False