import logging

import pyspark.sql.functions as F
from pyspark.sql import SparkSession

from domain.transformations.gold.temperature import transform
from infrastructure.config import Settings
from infrastructure.config.layers import Layer

logger = logging.getLogger(__name__)


def run_hourly_temperature_summary(spark: SparkSession, settings: Settings) -> None:
    df_silver = (
        spark.readStream
        .format("delta")
        .load(settings.delta_path(Layer.SILVER, "temperature"))
    )

    df_gold = transform(df_silver)

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
