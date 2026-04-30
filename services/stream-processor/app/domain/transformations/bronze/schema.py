from pyspark.sql.types import StructType, StructField, BinaryType, StringType, LongType, IntegerType, TimestampType


def get_schema() -> StructType:
    return StructType([
        StructField("key", BinaryType(), nullable=True),
        StructField("value", BinaryType(), nullable=True),
        StructField("topic", StringType(), nullable=True),
        StructField("partition", IntegerType(), nullable=True),
        StructField("offset", LongType(), nullable=True),
        StructField("timestamp", TimestampType(), nullable=True),
        StructField("timestampType", IntegerType(), nullable=True),
    ])
