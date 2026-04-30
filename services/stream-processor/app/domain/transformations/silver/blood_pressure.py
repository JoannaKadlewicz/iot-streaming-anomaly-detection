from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from domain.transformations.silver.common import filter_by_metric, add_audit_columns, select_base_columns


def _filter(df: DataFrame) -> DataFrame:
    return filter_by_metric(df, "blood_pressure")


def _enrich(df: DataFrame) -> DataFrame:
    return (df.transform(add_audit_columns)
            .withColumn("diastolic", F.split(F.col("value"), "-")[1].cast("integer"))
            .withColumn("systolic", F.split(F.col("value"), "-")[0].cast("integer"))
            .withColumn("pulse_pressure", F.col("systolic") - F.col("diastolic")))


def _select(df: DataFrame) -> DataFrame:
    return select_base_columns(df, ["systolic", "diastolic", "unit", "pulse_pressure"])


def transform(df: DataFrame) -> DataFrame:
    return df.transform(_filter).transform(_enrich).transform(_select)
