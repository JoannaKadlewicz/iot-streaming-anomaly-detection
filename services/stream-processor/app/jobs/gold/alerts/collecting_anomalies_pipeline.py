import logging

import pyspark.sql.functions as F
from pyspark.sql import SparkSession

from infrastructure.config import Settings
from infrastructure.config.layers import Layer

logger = logging.getLogger(__name__)


def run_collecting_anomalies(spark: SparkSession, settings: Settings) -> None:

    for metric, layer_name in [
        ("heart_rate", "heart_rate_summary"),
        ("blood_pressure", "blood_pressure_summary"),
        ("temperature", "temperature_hourly_summary"),
        ("steps", "steps_daily_summary"),
    ]:
        df = (
            spark.readStream
            .format("delta")
            .load(settings.delta_path(Layer.GOLD, layer_name))
            .filter(F.col("is_anomaly") == True)
            .select(
                F.col("account_id"),
                F.col("device_id"),
                F.lit(metric).alias("metric"),
                F.col("window_start"),
                F.col("window_end"),
                F.col("anomaly_reason"))
            .withColumn("alert_sent", F.lit(False))
            .withColumn("anomaly_id", F.expr("uuid()"))
        )

        q = (
            df.writeStream
            .queryName(f"anomalies_{metric}")
            .format("delta")
            .outputMode("append")
            .option("checkpointLocation", settings.checkpoint_path(Layer.GOLD, f"anomalies_{metric}"))
            .trigger(availableNow=True)
            .start(settings.delta_path(Layer.GOLD, "anomalies"))
        )

        q.awaitTermination()