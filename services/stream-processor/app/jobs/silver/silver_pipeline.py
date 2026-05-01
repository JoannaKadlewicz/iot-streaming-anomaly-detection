import logging

from pyspark.sql import SparkSession, DataFrame

from domain.transformations.silver.common import parse_metric
from domain.transformations.silver.registry import METRICS_TRANSFORMS
from infrastructure.config import Settings
from infrastructure.config.layers import Layer

logger = logging.getLogger(__name__)


def run_silver_transformation(spark: SparkSession, settings: Settings) -> None:
    df_bronze = (
        spark.readStream
        .format("delta")
        .load(settings.delta_path(Layer.BRONZE, "raw_metrics"))
    )

    query = (
        df_bronze.writeStream
        .foreachBatch(_process_batch(settings))
        .trigger(processingTime="60 seconds")
        .option("checkpointLocation", settings.checkpoint_path(Layer.SILVER, "metrics"))
        .start()
    )

    logger.info("Silver multiplexer started...")
    query.awaitTermination()


def _process_batch(settings: Settings):
    def process_batch(df: DataFrame, batch_id: int):
        logger.info("Processing silver batch=%d", batch_id)
        parsed_df = parse_metric(df).cache()

        for metric_type, transform_fn in METRICS_TRANSFORMS.items():
            path = settings.delta_path(Layer.SILVER, metric_type)
            try:
                transformed_df = transform_fn(parsed_df)
                transformed_df.repartition(1).write \
                    .format("delta") \
                    .mode("append") \
                    .partitionBy("event_date") \
                    .save(path)

                logger.info("Written %s to %s", metric_type, Layer.SILVER)

            except Exception:
                logger.exception("Failed writing silver for metric_type=%s", metric_type)

        parsed_df.unpersist()

    return process_batch
