from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import DecimalType

from domain.transformations.silver.common import filter_by_metric, add_audit_columns, select_base_columns


def _filter(df: DataFrame) -> DataFrame:
    return filter_by_metric(df, "temperature")


def _enrich(df: DataFrame) -> DataFrame:
    return (df.transform(add_audit_columns)
            .withColumn("temperature",
                        F.when(F.col("unit") == "F", (F.col("value") - 32) * 5 / 9)
                        .otherwise(F.col("value")).cast(DecimalType(10, 2)))
            .withColumn("unit", F.lit("C")))

def _select(df: DataFrame) -> DataFrame:
    return select_base_columns(df, ["temperature", "unit"])


def transform(df: DataFrame) -> DataFrame:
    return df.transform(_filter).transform(_enrich).transform(_select)
