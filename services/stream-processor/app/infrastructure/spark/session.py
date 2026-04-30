from pyspark.sql import SparkSession

# from infrastructure.config import Conf

import infrastructure.config.settings
print(infrastructure.config.settings.__file__)
#             .appName(settings.app_name)
#             .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
#             .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
#             .config("spark.sql.streaming.checkpointLocation", settings.CHECKPOINT_LOCATION)
#             .master(settings.MASTER_URL)
#             .getOrCreate())
