import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from domain.transformations.silver.schema import get_event_schema


def parse_metric(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("v", F.from_json(F.col("value").cast("string"), get_event_schema()))
        .filter(F.col("v").isNotNull())
        .select("v.*", F.col("timestamp").alias("event_time"))
    )


def filter_by_metric(df: DataFrame, metric: str) -> DataFrame:
    return (df
            .filter(F.col("metric_type") == metric)
            .filter(F.col("value").isNotNull())
            .dropDuplicates(["event_id"]))


def add_audit_columns(df: DataFrame) -> DataFrame:
    return (df
            .withColumn("event_date", F.to_date("event_ts"))
            .withColumn("ingested_at", F.current_timestamp()))


def select_base_columns(df: DataFrame, extra_cols: list[str]) -> DataFrame:
    base_columns = [
        "event_id", "account_id", "device_id",
        "metric_type", "event_ts", "event_date", "ingested_at"
    ]
    return df.select(*base_columns, *extra_cols)
