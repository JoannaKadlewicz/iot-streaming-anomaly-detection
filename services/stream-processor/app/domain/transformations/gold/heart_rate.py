from pyspark.sql import DataFrame
import pyspark.sql.functions as F


def _add_heart_rate_zone(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "heart_rate",
        F.when(F.col("avg_rate") > F.lit(170), "CRITICAL")
        .when(F.col("avg_rate") > F.lit(140), "HIGH")
        .when(F.col("avg_rate") > F.lit(100), "ELEVATED")
        .when(F.col("avg_rate") >= F.lit(60), "NORMAL")
        .otherwise("RESTING")
    )


def _add_anomaly_flag(df: DataFrame) -> DataFrame:
    high_rate = F.col("max_rate") > F.lit(180)
    low_rate = F.col("min_rate") < F.lit(35)
    high_variability = F.col("stddev_rate") > F.lit(25)

    return (
        df
        .withColumn("is_anomaly", high_rate | low_rate | high_variability)
        .withColumn(
            "anomaly_reason",
            F.when(high_rate, F.lit("high_rate"))
            .when(low_rate, F.lit("low_rate"))
            .when(high_variability, F.lit("high_variability"))
            .otherwise(F.lit(None).cast("string"))
        ))


def transform(df: DataFrame) -> DataFrame:
    return (
        df
        .withWatermark("event_ts", "10 minutes")
        .groupBy(
            "account_id",
            "device_id",
            F.window("event_ts", "5 minutes").alias("window")
        )
        .agg(
            F.avg("rate").alias("avg_rate"),
            F.min("rate").alias("min_rate"),
            F.max("rate").alias("max_rate"),
            F.stddev("rate").alias("stddev_rate"),
            F.count("*").alias("event_count"),
        )
        .withColumn("window_start", F.col("window.start"))
        .withColumn("window_end", F.col("window.end"))
        .drop("window")
        .transform(_add_heart_rate_zone)
        .transform(_add_anomaly_flag))
