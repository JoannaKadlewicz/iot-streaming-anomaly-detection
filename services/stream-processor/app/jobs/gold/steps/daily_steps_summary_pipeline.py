import logging

from pyspark.sql import SparkSession

from domain.transformations.gold.steps import transform
from infrastructure.config import Settings
from infrastructure.config.layers import Layer

logger = logging.getLogger(__name__)


def run_daily_steps_summary(spark: SparkSession, settings: Settings) -> None:
    df_silver = (
        spark.readStream
        .format("delta")
        .load(settings.delta_path(Layer.SILVER, "steps"))
    )

    df_gold = transform(df_silver)

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
