import pyspark.sql.functions as F
from pyspark.sql import DataFrame


def _add_anomaly_flag(df: DataFrame) -> DataFrame:
    low_daily_steps = F.col("total_steps") < F.lit(5000)
    unrealistic_spike = F.col("max_steps_per_event") > F.lit(200)

    return (
        df
        .withColumn("is_anomaly", low_daily_steps | unrealistic_spike)
        .withColumn(
            "anomaly_reason",
            F.when(unrealistic_spike, F.lit("unrealistic_spike"))
            .when(low_daily_steps, F.lit("low_daily_steps"))
            .otherwise(F.lit(None).cast("string"))
        )
    )


def _add_activity_level(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "activity_level",
        F.when(F.col("total_steps") >= F.lit(10000), "ACTIVE")
        .when(F.col("total_steps") >= F.lit(5000), "MODERATE")
        .when(F.col("total_steps") >= F.lit(1000), "LOW")
        .otherwise("SEDENTARY")
    )


def transform(df: DataFrame) -> DataFrame:
    return (
        df
        .withWatermark("event_ts", "30 minutes")
        .groupBy(
            "account_id",
            "device_id",
            F.window("event_ts", "1 day").alias("window")
        ).agg(
            F.sum("steps").alias("total_steps"),
            F.max("steps").alias("max_steps_per_event"),
            F.avg("steps").alias("avg_steps"),
            F.count("*").alias("event_count"),
        )
        .withColumn("window_start", F.col("window.start"))
        .withColumn("window_end", F.col("window.end"))
        .drop("window")
        .transform(_add_activity_level)
        .transform(_add_anomaly_flag))
