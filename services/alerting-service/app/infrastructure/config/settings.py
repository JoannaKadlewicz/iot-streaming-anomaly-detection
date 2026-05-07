from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    # mail
    smtp_host: str
    smtp_port: int
    smtp_login: str
    smtp_password: str
    smtp_from: str
    smtp_to: str

    # app
    app_name: str
    log_level: str

    # spark
    master_url: str
    anomalies_delta_path: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )


def get_settings() -> Settings:
    return Settings()
