# domain/generators/blood_pressure.py
from datetime import datetime
from typing import Any

import numpy as np

from domain.generators.base import BaseMetricGenerator
from domain.generators.context import ActivityLevel, MetricContext

_ACTIVITY_SYS_BOOST: dict[ActivityLevel, tuple[float, float]] = {
    ActivityLevel.SLEEPING: (-8.0, -4.0),
    ActivityLevel.RESTING: (0.0, 0.0),
    ActivityLevel.WALKING: (8.0, 18.0),
    ActivityLevel.RUNNING: (25.0, 45.0),
    ActivityLevel.WORKOUT: (20.0, 40.0),
}

_ACTIVITY_DIA_BOOST: dict[ActivityLevel, tuple[float, float]] = {
    ActivityLevel.SLEEPING: (-5.0, -2.0),
    ActivityLevel.RESTING: (0.0, 0.0),
    ActivityLevel.WALKING: (4.0, 10.0),
    ActivityLevel.RUNNING: (10.0, 20.0),
    ActivityLevel.WORKOUT: (8.0, 18.0),
}


class BloodPressureGenerator(BaseMetricGenerator):
    generator_name = "Blood Pressure Generator"
    metric_type = "blood_pressure"
    unit = "mmHg"
    interval_seconds = 900

    def __init__(self, context: MetricContext) -> None:
        super().__init__(context)
        self.prev_sys = 118.0
        self.prev_dia = 76.0
        self.active_episode_steps = 0
        self.current_episode: str | None = None

    def next_event(self, at: datetime | None = None) -> dict[str, Any]:
        rng = self.context.rng
        activity = self.context.activity.level

        second_of_day = at.hour * 3600 + at.minute * 60 + at.second
        circadian = 4 * np.sin(2 * np.pi * second_of_day / 86400)

        sys_low, sys_high = _ACTIVITY_SYS_BOOST[activity]
        dia_low, dia_high = _ACTIVITY_DIA_BOOST[activity]
        activity_sys = float(rng.uniform(sys_low, sys_high))
        activity_dia = float(rng.uniform(dia_low, dia_high))

        systolic = 0.9 * self.prev_sys + 0.1 * (118 + circadian) + activity_sys + rng.normal(0, 1.5)
        diastolic = 0.9 * self.prev_dia + 0.1 * (76 + circadian * 0.5) + activity_dia + rng.normal(0, 1.0)

        if self.active_episode_steps == 0 and rng.random() < 0.002:
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

        event = self._base_event(at)
        event.update({
            "value": f"{systolic:.0f}-{diastolic:.0f}",
            "unit": self.unit,
        })
        return event
