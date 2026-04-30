from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    @computed_field
    @property
    def bronze_delta_path(self) -> str:
        return f"{self.delta_base_path}/bronze"

    @computed_field
    @property
    def silver_checkpoint_path(self) -> str:
        return f"{self.delta_base_path}/silver/checkpoint"

    def silver_path_for(self, metric_type: str) -> str:
        return f"{self.delta_base_path}/silver/{metric_type}"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[3] / ".env",
        env_file_encoding="utf-8",
    )


def get_settings() -> Settings:
    return Settings()
