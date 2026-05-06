from pyspark.sql import DataFrame
from pyspark.sql.functions import current_timestamp


def transform(df: DataFrame) -> DataFrame:
    return df.withColumn("ingested_at", current_timestamp())
