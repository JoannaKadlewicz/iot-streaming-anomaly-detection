import logging

from pyspark.sql import SparkSession

from domain.transformations.gold.heart_rate import transform
from infrastructure.config import Settings
from infrastructure.config.layers import Layer

logger = logging.getLogger(__name__)

def run_blood_pressure_summary(spark: SparkSession, settings: Settings) -> None:
    df_silver = (
        spark.readStream
        .format("delta")
        .load(settings.delta_path(Layer.SILVER, "blood_pressure"))
    )

    df_gold = df_silver.transform(transform)

    query = (
        df_gold.writeStream
        .queryName("gold_blood_pressure_summary")
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", settings.checkpoint_path(Layer.GOLD, "blood_pressure_summary"))
        .trigger(availableNow=True)
        .start(settings.delta_path(Layer.GOLD, "blood_pressure_summary"))
    )

    query.awaitTermination()