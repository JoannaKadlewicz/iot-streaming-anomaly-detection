import logging

import pyspark.sql.functions as F
from pyspark.sql import SparkSession

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
        .groupBy(
            "account_id",
            "device_id",
            F.window("event_ts", "1 minute").alias("window")
        ).agg(
            F.avg("temperature").alias("avg_temp"),
            F.min("temperature").alias("min_temp"),
            F.max("temperature").alias("max_temp"),
            F.stddev("temperature").alias("stddev_temp"),
            F.count("*").alias("event_count"),
        )
        .withColumn("window_start", F.col("window.start"))
        .withColumn("window_end", F.col("window.end"))
        .drop("window")

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
