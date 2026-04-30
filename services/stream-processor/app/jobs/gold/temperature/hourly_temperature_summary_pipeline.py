import logging

from pyspark.sql import SparkSession

from domain.transformations.gold.temperature.hourly_summary import transform
from infrastructure.config import Settings

logger = logging.getLogger(__name__)


def run_hourly_temperature_summary(spark: SparkSession, settings: Settings) -> None:
    df_silver = (
        spark.readStream
        .format("delta")
        .load(settings.silver_path_for("temperature"))
    )

    df_gold = (
        df_silver
        .withWatermark("event_ts", "10 minutes")
        .transform(transform)
    )

    query = (
        df_gold.writeStream
        .queryName("gold_temperature_hourly")
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", settings.checkpoint_path("gold"))
        .trigger(availableNow=True)
        .start(f'{settings.delta_base_path}/gold/temperature_hourly_summary')
    )

    query.awaitTermination()
    logger.info("[Gold] Hourly temperature summary finished.")