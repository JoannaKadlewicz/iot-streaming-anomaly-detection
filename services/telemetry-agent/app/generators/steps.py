from datetime import datetime
from typing import Any

from generators.base import BaseMetricGenerator
from generators.context import MetricContext


class StepsGenerator(BaseMetricGenerator):
    metric_type = "steps"
    unit = "count"

    def __init__(self, context: MetricContext) -> None:
        super().__init__(context)

    def next_event(self) -> dict[str, Any]:
        now = datetime.now()
        rng = self.context.rng

        hour = now.hour
        if 0 <= hour < 6:
            lam = 0.2
        elif 6 <= hour < 9:
            lam = 8
        elif 9 <= hour < 18:
            lam = 18
        elif 18 <= hour < 22:
            lam = 10
        else:
            lam = 2

        steps = int(rng.poisson(lam))

        if rng.random() < 0.003:
            if rng.random() < 0.5:
                steps = int(rng.integers(250, 600))
            else:
                steps = 0

        event = self._base_event(now)
        event.update({
            "value": steps,
            "unit": self.unit,
        })
        return event
