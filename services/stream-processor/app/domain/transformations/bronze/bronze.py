from pandas import DataFrame
from pyspark.sql.functions import current_timestamp


def apply_ingestion_timestamp(df: DataFrame) -> DataFrame:
    return df.withColumn("ingested_at", current_timestamp())