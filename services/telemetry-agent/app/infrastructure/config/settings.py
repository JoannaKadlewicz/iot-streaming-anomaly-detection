from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    # Kafka
    kafka_bootstrap_server: str
    kafka_topic: str

    # App
    echo: bool
    log_level: str
    file_source: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )


def get_settings() -> Settings:
    return Settings()
