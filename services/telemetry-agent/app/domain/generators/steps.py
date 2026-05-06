from datetime import datetime
from typing import Any

from domain.generators.base import BaseMetricGenerator
from domain.generators.context import ActivityLevel, MetricContext

_STEPS_PER_MINUTE: dict[ActivityLevel, tuple[float, float]] = {
    ActivityLevel.SLEEPING: (0.0, 0.0),
    ActivityLevel.RESTING: (0.0, 1.0),
    ActivityLevel.WALKING: (40.0, 80.0),
    ActivityLevel.RUNNING: (120.0, 180.0),
    ActivityLevel.WORKOUT: (20.0, 90.0)
}


class StepsGenerator(BaseMetricGenerator):
    generator_name = "Steps Generator"
    metric_type = "steps"
    unit = "count/min"
    interval_seconds = 60

    def __init__(self, context: MetricContext) -> None:
        super().__init__(context)

    def next_event(self, at: datetime | None = None) -> dict[str, Any]:
        now = at or datetime.now()
        rng = self.context.rng
        activity = self.context.activity.level

        low, high = _STEPS_PER_MINUTE[activity]

        if low == 0.0 and high == 0.0:
            steps = 0
        else:
            steps_per_min = rng.uniform(low, high)
            lam = steps_per_min * (self.interval_seconds / 60.0)
            steps = int(rng.poisson(lam))

        event = self._base_event(now)
        event.update({
            "value": steps,
            "unit": self.unit,
        })
        return event
