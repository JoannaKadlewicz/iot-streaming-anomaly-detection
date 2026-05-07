import logging

from infrastructure.config.layers import Layer
from infrastructure.config.logging import configure_logging
from infrastructure.config.settings import get_settings
from infrastructure.spark import create_spark_session

logger = logging.getLogger(__name__)


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    spark = create_spark_session(settings)

    (spark.read
     .format("delta")
     .load(settings.delta_path(Layer.GOLD, "XXX"))
     .show(5, truncate=False))


if __name__ == "__main__":
    main()
