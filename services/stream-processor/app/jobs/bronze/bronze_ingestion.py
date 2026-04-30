from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql.types import StructType

from domain.transformations.bronze import apply_ingestion_timestamp, get_schema
from infrastructure.config import Settings


def run_bronze_ingestion(spark: SparkSession, settings: Settings) -> None:

    schema: StructType = get_schema()

    df_raw: DataFrame = (
        spark.readStream
        .format("kafka")
        .schema(schema)
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
        .option("checkpointLocation", f"{settings.checkpoint_base_path}/bronze")
        .option("mergeSchema", False)
        .trigger(processingTime="30 seconds")
        .start(path=f"{settings.delta_base_path}/bronze")
    )

    query.awaitTermination()
