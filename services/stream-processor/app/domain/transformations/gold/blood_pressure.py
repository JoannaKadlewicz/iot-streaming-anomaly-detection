from pyspark.sql import DataFrame
import pyspark.sql.functions as F


def add_bp_category(df: DataFrame) -> DataFrame:
    crisis    = (F.col("max_systolic") >= F.lit(180)) | (F.col("max_diastolic") >= F.lit(120))
    ht2       = (F.col("avg_systolic") >= F.lit(140)) | (F.col("avg_diastolic") >= F.lit(90))
    ht1       = (F.col("avg_systolic") >= F.lit(130)) | (F.col("avg_diastolic") >= F.lit(80))
    elevated  = (F.col("avg_systolic") >= F.lit(120)) & (F.col("avg_diastolic") <F.lit( 80))

    return df.withColumn(
        "bp_category",
        F.when(crisis,"CRISIS")
         .when(ht2,"HT_STAGE2")
         .when(ht1,"HT_STAGE1")
         .when(elevated,"ELEVATED")
         .otherwise("NORMAL")
    )


def add_anomaly_flag(df: DataFrame) -> DataFrame:
    hypertensive_crisis = F.col("bp_category").isin("CRISIS", "HT_STAGE2")
    hypotension         = F.col("min_systolic") < F.lit(80)
    wide_pulse_pressure = F.col("avg_pulse_pressure") > F.lit(60)

    return (
        df
        .withColumn(
            "is_anomaly",
            hypertensive_crisis | hypotension | wide_pulse_pressure
        )
        .withColumn(
            "anomaly_reason",
            F.when(hypertensive_crisis, F.lit("hypertensive_crisis"))
             .when(hypotension,         F.lit("hypotension"))
             .when(wide_pulse_pressure, F.lit("wide_pulse_pressure"))
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
            F.window("event_ts", "15 minutes").alias("window")
        )
        .agg(
            F.avg("systolic").alias("avg_systolic"),
            F.min("systolic").alias("min_systolic"),
            F.max("systolic").alias("max_systolic"),
            F.avg("diastolic").alias("avg_diastolic"),
            F.max("diastolic").alias("max_diastolic"),
            F.avg("pulse_pressure").alias("avg_pulse_pressure"),
            F.count("*").alias("event_count"),
        )
        .withColumn("window_start", F.col("window.start"))
        .withColumn("window_end",   F.col("window.end"))
        .drop("window")
        .transform(add_bp_category)
        .transform(add_anomaly_flag)
    )