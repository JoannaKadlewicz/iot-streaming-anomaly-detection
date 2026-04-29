from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    # Database
    db_host: str
    db_port: int
    db_database_name: str
    db_username: str
    db_password: str

    # Kafka
    kafka_bootstrap_server: str
    kafka_topic: str

    # App
    account_id: int
    debug: bool

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )

    @computed_field
    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+psycopg://{self.db_username}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_database_name}"
        )


def get_settings() -> Settings:
    return Settings()
