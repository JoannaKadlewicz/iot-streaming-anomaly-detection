from datetime import datetime
from typing import Any

from generators.base import BaseMetricGenerator
from generators.context import MetricContext


class StepsGenerator(BaseMetricGenerator):
    metric_type = "steps"
    unit = "count"

    def __init__(self, context: MetricContext, interval_seconds: int = 60) -> None:
        super().__init__(context)
        self.interval_seconds = interval_seconds

    def next_event(self) -> dict[str, Any]:
        now = datetime.utcnow()
        rng = self.context.rng

        hour = now.hour

        if 0 <= hour < 6:
            steps_per_minute = 1
        elif 6 <= hour < 9:
            steps_per_minute = 20
        elif 9 <= hour < 18:
            steps_per_minute = 35
        elif 18 <= hour < 22:
            steps_per_minute = 18
        else:
            steps_per_minute = 5

        lam = steps_per_minute * (self.interval_seconds / 60.0)
        steps = int(rng.poisson(lam))

        if rng.random() < 0.003:
            if rng.random() < 0.5:
                steps += int(rng.integers(80, 250))
            else:
                steps = 0

        event = self._base_event(now)
        event.update({
            "value": steps,
            "unit": self.unit,
            "interval_seconds": self.interval_seconds,
        })
        return event