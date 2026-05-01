import logging

from pyspark.sql import SparkSession

from domain.transformations.gold.temperature.hourly_summary import transform
from infrastructure.config import Settings
from infrastructure.config.layers import Layer

logger = logging.getLogger(__name__)


def run_hourly_temperature_summary(spark: SparkSession, settings: Settings) -> None:
    df_silver = (
        spark.readStream
        .format("delta")
        .load(settings.delta_path(Layer.SILVER, "temperature"))
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
        .option("checkpointLocation", settings.checkpoint_path(Layer.GOLD, "temperature_hourly_summary"))
        .trigger(availableNow=True)
        .start(settings.delta_path(Layer.GOLD, "temperature_hourly_summary"))
    )

    query.awaitTermination()
