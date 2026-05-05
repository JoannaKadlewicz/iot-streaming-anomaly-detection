import logging

from delta import DeltaTable

from infrastructure.config.layers import Layer
from infrastructure.config.settings import get_settings
from infrastructure.spark import create_spark_session

logger = logging.getLogger(__name__)


def main():
    settings = get_settings()

    spark = create_spark_session(settings)

    delta_tables = [
        settings.delta_path(Layer.BRONZE, "raw_metrics")
    ]

    for table in delta_tables:
        logger.info("Optimizing %s", table)
        DeltaTable.forPath(spark, table).optimize().executeCompaction()
        logger.info("Done: %s", table)


if __name__ == "__main__":
    main()
