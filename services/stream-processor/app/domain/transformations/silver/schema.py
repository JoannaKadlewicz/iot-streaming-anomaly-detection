from pyspark.sql.types import StructType, StructField, StringType, TimestampType, \
    DateType


def get_event_schema() -> StructType:
    return StructType([
        StructField("event_id", StringType(), nullable=False),
        StructField("account_id", StringType(), nullable=False),
        StructField("device_id", StringType(), nullable=False),
        StructField("metric_type", StringType(), nullable=False),
        StructField("event_ts", TimestampType(), nullable=False),
        StructField("event_date", DateType(), nullable=False),
        StructField("ingested_at", TimestampType(), nullable=False),
        StructField("value", StringType(), nullable=False),
        StructField("unit", StringType(), nullable=False),
    ])
