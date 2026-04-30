from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from domain.transformations.silver.common import filter_by_metric, add_audit_columns, select_base_columns


def _filter(df: DataFrame) -> DataFrame:
    return filter_by_metric(df, "steps")


def _enrich(df: DataFrame) -> DataFrame:
    return (df.transform(add_audit_columns)
            .withColumn("steps", F.col("value").cast("integer")))


def _select(df: DataFrame) -> DataFrame:
    return select_base_columns(df, ["steps", "unit"])


def transform(df: DataFrame) -> DataFrame:
    return df.transform(_filter).transform(_enrich).transform(_select)
