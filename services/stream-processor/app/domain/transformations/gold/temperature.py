import pyspark.sql.functions as F
from pyspark.sql import DataFrame


def add_temp_category(df: DataFrame) -> DataFrame:
    hyperthermia = F.col("max_temp") >= F.lit(38.0)
    high_fever = F.col("max_temp") >= F.lit(39.5)
    hypothermia = F.col("min_temp") < F.lit(35.0)

    return df.withColumn(
        "temp_category",
        F.when(high_fever, "HIGH_FEVER")
        .when(hyperthermia, "FEVER")
        .when(hypothermia, "HYPOTHERMIA")
        .otherwise("NORMAL")
    )


def add_anomaly_flag(df: DataFrame) -> DataFrame:
    fever = F.col("temp_category").isin("FEVER", "HIGH_FEVER")
    hypothermia = F.col("temp_category") == F.lit("HYPOTHERMIA")
    high_stddev = F.col("stddev_temp") > F.lit(0.5)

    return (
        df
        .withColumn(
            "is_anomaly",
            fever | hypothermia | high_stddev
        )
        .withColumn(
            "anomaly_reason",
            F.when(fever, F.lit("fever"))
            .when(hypothermia, F.lit("hypothermia"))
            .when(high_stddev, F.lit("unstable_readings"))
            .otherwise(F.lit(None).cast("string"))
        )
    )


def transform(df: DataFrame) -> DataFrame:
    return (
        df
        .withWatermark("event_ts", "10 minutes")
        .groupBy(
            "account_id",
            "device_id",
            F.window("event_ts", "60 minutes").alias("window")
        )
        .agg(
            F.avg("temperature").alias("avg_temp"),
            F.min("temperature").alias("min_temp"),
            F.max("temperature").alias("max_temp"),
            F.stddev("temperature").alias("stddev_temp"),
            F.count("*").alias("event_count"),
        )
        .withColumn("window_start", F.col("window.start"))
        .withColumn("window_end", F.col("window.end"))
        .drop("window")
        .transform(add_temp_category)
        .transform(add_anomaly_flag)
    )
