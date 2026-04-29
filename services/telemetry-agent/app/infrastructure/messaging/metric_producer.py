import json
from typing import Any

from kafka import KafkaProducer

MESSAGE_ENCODING = "utf-8"


class MetricProducer:

    def __init__(self, bootstrap_servers: str, topic: str):
        self.topic = topic
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda value: json.dumps(value).encode(MESSAGE_ENCODING),
            key_serializer=lambda key: key.encode(MESSAGE_ENCODING),
        )

    def send_metric(self, metric: dict[str, Any], key: int) -> None:
        self._producer.send(self.topic, value=metric, key=str(key))

    def flush(self) -> None:
        self._producer.flush()

    def close(self) -> None:
        self._producer.close()
