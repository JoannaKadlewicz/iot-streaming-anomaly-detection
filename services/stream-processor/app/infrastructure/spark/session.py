from pyspark.sql import SparkSession

from infrastructure.config import Settings


def create_spark_session(settings: Settings) -> SparkSession:
    return (SparkSession.builder
            .appName(settings.app_name)
            .master(settings.master_url)
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .config("spark.jars.packages",
                    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,"
                    "io.delta:delta-spark_2.12:3.2.0")
            .getOrCreate())
