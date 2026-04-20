from datetime import datetime
from typing import Any

import numpy as np

from generators.base import BaseMetricGenerator
from generators.context import MetricContext


class BloodPressureGenerator(BaseMetricGenerator):
    metric_type = "blood_pressure"
    unit = "mmHg"

    def __init__(self, context: MetricContext) -> None:
        super().__init__(context)
        self.prev_sys = 118.0
        self.prev_dia = 76.0
        self.active_episode_steps = 0
        self.current_episode: str | None = None

    def next_event(self) -> dict[str, Any]:
        now = datetime.now()
        rng = self.context.rng

        second_of_day = now.hour * 3600 + now.minute * 60 + now.second
        circadian = 4 * np.sin(2 * np.pi * second_of_day / 86400)

        systolic = 0.9 * self.prev_sys + 0.1 * (118 + circadian) + rng.normal(0, 1.5)
        diastolic = 0.9 * self.prev_dia + 0.1 * (76 + circadian * 0.5) + rng.normal(0, 1.0)

        if self.active_episode_steps == 0 and rng.random() < 0.003:
            self.active_episode_steps = int(rng.integers(6, 16))
            self.current_episode = str(rng.choice(["high_bp_episode", "low_bp_episode"]))

        if self.active_episode_steps > 0:
            self.active_episode_steps -= 1

            if self.current_episode == "high_bp_episode":
                systolic += float(rng.uniform(20, 45))
                diastolic += float(rng.uniform(10, 25))
            else:
                systolic -= float(rng.uniform(20, 35))
                diastolic -= float(rng.uniform(10, 20))

            if self.active_episode_steps == 0:
                self.current_episode = None

        systolic = int(np.clip(round(systolic), 70, 220))
        diastolic = int(np.clip(round(diastolic), 40, 140))

        self.prev_sys = float(systolic)
        self.prev_dia = float(diastolic)

        event = self._base_event(now)
        event.update({
            "systolic": systolic,
            "diastolic": diastolic,
            "unit": self.unit,
        })
        return event
