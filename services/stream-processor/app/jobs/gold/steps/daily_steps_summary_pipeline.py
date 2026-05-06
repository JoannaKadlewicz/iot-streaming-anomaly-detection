import logging

import pyspark.sql.functions as F
from pyspark.sql import SparkSession

from infrastructure.config import Settings
from infrastructure.config.layers import Layer

logger = logging.getLogger(__name__)


def run_daily_steps_summary(spark: SparkSession, settings: Settings) -> None:
    df_silver = (
        spark.readStream
        .format("delta")
        .load(settings.delta_path(Layer.SILVER, "steps"))
    )

    df_gold = (
        df_silver
        .withWatermark("event_ts", "10 minutes")
        .groupBy(
            "account_id",
            "device_id",
            F.window("event_ts", "1 day").alias("window")
        ).agg(
            F.sum("steps").alias("steps_count")
        )
        .withColumn("window_start", F.col("window.start"))
        .withColumn("window_end", F.col("window.end"))
        .drop("window")
    )

    query = (
        df_gold.writeStream
        .queryName(f"{Layer.GOLD}_steps_daily_summary")
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", settings.checkpoint_path(Layer.GOLD, "steps_daily_summary"))
        .trigger(availableNow=True)
        .start(settings.delta_path(Layer.GOLD, "steps_daily_summary"))
    )

    query.awaitTermination()
