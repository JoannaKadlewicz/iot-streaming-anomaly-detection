import pyspark.sql.functions as F
from pyspark.sql import SparkSession

from domain.model.anomaly import Anomaly


class AnomalyReader:
    def __init__(self, spark: SparkSession, anomalies_delta_path: str):
        self._spark = spark
        self._anomalies_delta_path = anomalies_delta_path

    def fetch_unsent(self) -> list[Anomaly]:
        anomalies = (
            self._spark.read.format("delta")
            .load(self._anomalies_delta_path)
            .filter(F.col("alert_sent") == False)
            .collect())

        return [
            Anomaly(
                account_id=anomaly.account_id,
                device_id=anomaly.device_id,
                metric=anomaly.metric,
                anomaly_reason=anomaly.anomaly_reason,
                window_start=anomaly.window_start,
                window_end=anomaly.window_end,
                alert_sent=anomaly.alert_sent,
            )
            for anomaly in anomalies
        ]
