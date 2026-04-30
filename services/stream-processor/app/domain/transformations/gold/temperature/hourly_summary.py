from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def _aggregate(df: DataFrame) -> DataFrame:
    return (
        df.groupBy(
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
        .withColumn("window_end",   F.col("window.end"))
        .drop("window")
    )


def transform(df: DataFrame) -> DataFrame:
    return df.transform(_aggregate)
