import pyspark.sql.functions as F
from delta import DeltaTable
from pyspark.sql import SparkSession

from domain.model.anomaly import Anomaly


class AnomalyStatusWriter:

    def __init__(self, spark: SparkSession, anomalies_delta_path: str):
        self._table = DeltaTable.forPath(spark, anomalies_delta_path)

    def mark_as_sent(self, anomaly: Anomaly) -> None:
        self._table.update(
            condition=(
                    F.col("anomaly_id") == F.lit(anomaly.anomaly_id)
            ),
            set={
                "alert_sent": F.lit(True)
            }
        )
