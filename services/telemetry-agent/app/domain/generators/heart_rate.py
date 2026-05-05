# domain/generators/heart_rate.py
from datetime import datetime
from typing import Any

import numpy as np

from domain.generators.base import BaseMetricGenerator
from domain.generators.context import ActivityLevel, MetricContext

_ACTIVITY_HR: dict[ActivityLevel, tuple[float, float]] = {
    ActivityLevel.SLEEPING: (45.0, 60.0),
    ActivityLevel.RESTING: (60.0, 80.0),
    ActivityLevel.WALKING: (90.0, 110.0),
    ActivityLevel.RUNNING: (140.0, 170.0),
    ActivityLevel.WORKOUT: (120.0, 160.0),
}


class HeartRateGenerator(BaseMetricGenerator):
    generator_name = "Heart Rate Generator"
    metric_type = "heart_rate"
    unit = "bpm"
    interval_seconds = 5

    def __init__(self, context: MetricContext) -> None:
        super().__init__(context)
        self.prev_hr = 72.0
        self.active_episode_steps = 0
        self.current_episode: str | None = None

    def next_event(self, at: datetime | None = None) -> dict[str, Any]:
        rng = self.context.rng
        activity = self.context.activity.level

        target_low, target_high = _ACTIVITY_HR[activity]
        target_hr = float(rng.uniform(target_low, target_high))

        noise = rng.normal(0, 1.5)
        hr = 0.85 * self.prev_hr + 0.15 * target_hr + noise

        if self.active_episode_steps == 0 and rng.random() < 0.001:
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

        event = self._base_event(at)
        event.update({
            "value": hr,
            "unit": self.unit,
        })
        return event
