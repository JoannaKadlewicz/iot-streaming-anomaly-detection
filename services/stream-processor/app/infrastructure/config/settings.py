from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):

    # Spark
    app_name: str
    master_url: str
    checkpoint_url: str

    # App
    log_level: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )


def get_settings() -> Settings:
    return Settings()
