from datetime import datetime
from typing import Any

import numpy as np

from generators.base import BaseMetricGenerator
from generators.context import MetricContext


class HeartRateGenerator(BaseMetricGenerator):
    metric_type = "heart_rate"
    unit = "bpm"

    def __init__(self, context: MetricContext) -> None:
        super().__init__(context)
        self.prev_hr = 72.0
        self.activity_boost = 0.0
        self.active_episode_steps = 0
        self.current_episode: str | None = None

    def next_event(self) -> dict[str, Any]:
        now = datetime.utcnow()
        rng = self.context.rng

        if rng.random() < 0.05:
            self.activity_boost = float(rng.uniform(8, 35))
        else:
            self.activity_boost *= 0.85

        baseline = 68 + self.activity_boost
        noise = rng.normal(0, 1.8)
        hr = 0.85 * self.prev_hr + 0.15 * baseline + noise

        if self.active_episode_steps == 0 and rng.random() < 0.004:
            self.active_episode_steps = int(rng.integers(5, 15))
            self.current_episode = str(rng.choice(["high_hr_episode", "low_hr_episode"]))

        if self.active_episode_steps > 0:
            self.active_episode_steps -= 1

            if self.current_episode == "low_hr_episode":
                hr -= float(rng.uniform(20, 35))
            else:
                hr += float(rng.uniform(35, 70))

            if self.active_episode_steps == 0:
                self.current_episode = None

        hr = int(np.clip(round(hr), 35, 210))
        self.prev_hr = float(hr)

        event = self._base_event(now)
        event.update({
            "value": hr,
            "unit": self.unit,
        })
        return event
