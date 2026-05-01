import logging

from infrastructure.config.logging import configure_logging
from infrastructure.config.settings import get_settings
from infrastructure.spark import create_spark_session
from jobs.gold.temperature.hourly_temperature_summary_pipeline import run_hourly_temperature_summary

logger = logging.getLogger(__name__)

def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    spark = create_spark_session(settings)

    logger.info("[GOLD] Starting hourly temperature summary...")
    run_hourly_temperature_summary(spark, settings)
    logger.info("[Gold] Hourly temperature summary finished.")
    # spark.read.format("delta").load(f'{settings.delta_base_path}/gold/temperature_hourly_summary').filter(col("device_id") == 2).show(1000, truncate=False)


if __name__ == "__main__":
    main()
