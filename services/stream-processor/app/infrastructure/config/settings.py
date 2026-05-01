from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from infrastructure.config.layers import Layer


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

    def checkpoint_path(self, layer: Layer, checkpoint_name: str) -> str:
        return f"{self.checkpoint_base_path}/{layer}/{checkpoint_name}"

    def delta_path(self, layer: Layer, table_name: str) -> str:
        return f"{self.delta_base_path}/{layer}/{table_name}"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[3] / ".env",
        env_file_encoding="utf-8",
    )


def get_settings() -> Settings:
    return Settings()
