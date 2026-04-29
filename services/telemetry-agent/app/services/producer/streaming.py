from time import sleep

from infrastructure.messaging.metric_producer import MetricProducer
from domain.generators.base import BaseMetricGenerator
import logging

logger = logging.getLogger(__name__)
EVENT_THRESHOLD = 50

def stream(
    producer: MetricProducer,
    generators: list[BaseMetricGenerator],
    delay_interval: float = .5,
) -> None:
    event_counter = 0
    while True:
        for generator in generators:
            metric = generator.next_event()
            producer.send_metric(metric=metric, key=metric["device_id"])
            event_counter += 1

        if event_counter >= EVENT_THRESHOLD:
            logger.info("Flushing %s metrics to the queue", EVENT_THRESHOLD)
            producer.flush()
            event_counter = 0

        sleep(delay_interval)