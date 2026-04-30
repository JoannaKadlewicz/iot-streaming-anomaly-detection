import logging

from infrastructure.config.logging import configure_logging
from infrastructure.config.settings import get_settings
from infrastructure.spark import create_spark_session

logger = logging.getLogger(__name__)

def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    spark = create_spark_session(settings)

    logger.info("Starting silver layer")

    silver_df = (
        spark.read
        .format("delta")
        .load(settings.silver_path_for("blood_pressure"))
    )

    silver_df.show(50, truncate=False)

if __name__ == "__main__":
    main()
