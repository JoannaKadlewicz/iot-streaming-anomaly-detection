import logging
from collections import Counter
from datetime import datetime, timedelta

from domain.generators.base import BaseMetricGenerator
from domain.generators.context import MetricContext
from infrastructure.messaging import MetricProducer

logger = logging.getLogger(__name__)


def generate_backfill(
        generators: list[BaseMetricGenerator],
        start: datetime,
        end: datetime,
        metric_producer: MetricProducer,
) -> int:
    current: dict[int, datetime] = {
        id(g): start for g in generators
    }

    last_transition: dict[int, datetime] = {
        g.context.device_id: start for g in generators
    }

    gen_by_id: dict[int, BaseMetricGenerator] = {id(g): g for g in generators}

    event_count = 0

    activity_counter: Counter = Counter()
    while True:
        next_gen_id = min(current, key=lambda k: current[k])
        ts = current[next_gen_id]

        if ts >= end:
            break

        gen = gen_by_id[next_gen_id]
        ctx: MetricContext = gen.context

        last_ts = last_transition[ctx.device_id]
        if (ts - last_ts).total_seconds() >= 60:
            ctx.activity.transition(ctx.rng, ts.hour)
            last_transition[ctx.device_id] = ts
            logger.debug(
                "Activity transition device=%s ts=%s → %s",
                ctx.device_id,
                ts.isoformat(),
                ctx.activity.level,
            )
        activity_counter[gen.context.activity.level.value] += 1
        event = gen.next_event(at=ts)

        metric_producer.send_metric(event, gen.context.device_id)

        event_count += 1

        if event_count % 100_000 == 0:
            logger.info("Generated %d events, current ts: %s", event_count, ts)
            metric_producer.flush()

        current[next_gen_id] = ts + timedelta(seconds=gen.interval_seconds)

    total = sum(activity_counter.values())
    for level, count in sorted(activity_counter.items(), key=lambda x: -x[1]):
        logger.info("Activity %-10s: %6d  (%.1f%%)", level, count, count / total * 100)
    logger.info("Backfill complete: %d events written to queue", event_count)
    return event_count
