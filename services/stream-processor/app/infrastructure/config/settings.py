from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"

print(ENV_FILE)


class Settings(BaseSettings):
    # Spark
    app_name: str
    master_url: str
    base_path: str
    checkpoint_base_path: str
    delta_base_path: str

    # Kafka
    kafka_bootstrap_server: str
    kafka_topic: str

    # App
    log_level: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )


def get_settings() -> Settings:
    return Settings()
