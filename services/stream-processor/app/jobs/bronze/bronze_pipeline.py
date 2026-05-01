from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.streaming import StreamingQuery

from domain.transformations.bronze.bronze import apply_ingestion_timestamp
from infrastructure.config import Settings
from infrastructure.config.layers import Layer


def run_bronze_ingestion(spark: SparkSession, settings: Settings) -> None:
    df_raw: DataFrame = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", settings.kafka_bootstrap_server)
        .option("subscribe", settings.kafka_topic)
        .option("startingOffsets", "latest")
        .load()
    )

    df_transformed: DataFrame = apply_ingestion_timestamp(df_raw)

    query: StreamingQuery = (
        df_transformed.writeStream
        .queryName("bronze_ingestion")
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", settings.checkpoint_path(Layer.BRONZE, "raw_metrics"))
        .option("mergeSchema", False)
        .trigger(processingTime="30 seconds")
        .start(settings.delta_path(Layer.BRONZE, "raw_metrics"))
    )

    query.awaitTermination()
