import heapq
import logging
from dataclasses import dataclass, field
from datetime import datetime
from time import sleep, time

from domain.generators import MetricContext
from domain.generators.base import BaseMetricGenerator
from infrastructure.messaging import MetricProducer

logger = logging.getLogger(__name__)
EVENT_THRESHOLD = 1024


@dataclass(order=True)
class ScheduledGenerator:
    next_tick: float
    generator: BaseMetricGenerator = field(compare=False)


def stream(
        producer: MetricProducer,
        generators: list[BaseMetricGenerator],
        realtime: bool = True,
) -> None:
    queue = [ScheduledGenerator(next_tick=time(), generator=g) for g in generators]
    heapq.heapify(queue)

    last_transition: dict[str, float] = {}
    TRANSITION_INTERVAL = 60.0

    while True:
        item = heapq.heappop(queue)
        now = time()

        if realtime and item.next_tick > now:
            sleep(item.next_tick - now)

        ctx: MetricContext = item.generator.context
        ctx_key = str(ctx.device_id)
        if now - last_transition.get(ctx_key, 0) >= TRANSITION_INTERVAL:
            hour = datetime.now().hour
            ctx.activity.transition(ctx.rng, hour)
            last_transition[ctx_key] = now
            logger.info(
                "Activity transition for device %s → %s",
                ctx_key,
                ctx.activity.level,
            )

        metric = item.generator.next_event()
        producer.send_metric(metric=metric, key=metric["device_id"])

        logger.info(metric)
        item.next_tick += item.generator.interval_seconds
        heapq.heappush(queue, item)
