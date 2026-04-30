import logging

from infrastructure.config.logging import configure_logging
from infrastructure.config.settings import get_settings
from infrastructure.spark import create_spark_session
from jobs.silver.silver_pipeline import run_silver_transformation

logger = logging.getLogger(__name__)

def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    spark = create_spark_session(settings)

    logger.info("Starting silver layer")

    run_silver_transformation(spark, settings)

if __name__ == "__main__":
    main()
