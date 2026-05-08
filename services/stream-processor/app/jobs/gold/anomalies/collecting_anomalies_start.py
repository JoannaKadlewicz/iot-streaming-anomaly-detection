import logging

from infrastructure.config.logging import configure_logging
from infrastructure.config.settings import get_settings
from infrastructure.spark import create_spark_session
from jobs.gold.anomalies.collecting_anomalies_pipeline import run_collecting_anomalies

logger = logging.getLogger(__name__)


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    spark = create_spark_session(settings)
    logger.info("[GOLD] Starting collecting anomalies...")

    run_collecting_anomalies(spark, settings)

if __name__ == "__main__":
    main()
