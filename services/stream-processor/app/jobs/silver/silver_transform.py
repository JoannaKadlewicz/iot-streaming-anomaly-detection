from pyspark.sql import SparkSession

from infrastructure.config import Settings


def run_silver_transformation(spark: SparkSession, settings: Settings):
    raw_df = (
        spark.read
        .parquet(f"{settings.delta_base_path}/bronze")
    )

    raw_df.printSchema()
    raw_df.show(5, truncate=False)



    pass
