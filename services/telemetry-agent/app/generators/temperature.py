from datetime import datetime
from typing import Literal, Any

import numpy as np

from generators.base import BaseMetricGenerator
from generators.context import MetricContext


class BodyTemperatureGenerator(BaseMetricGenerator):
    metric_type = "temperature"
    TemperatureUnit = Literal["C", "F"]

    def __init__(
        self,
        context: MetricContext,
        unit: TemperatureUnit = "C",
    ) -> None:
        super().__init__(context)

        if unit not in {"C", "F"}:
            raise ValueError("unit must be 'C' or 'F'")

        self.unit = unit
        self.prev_base_temp_c = 36.6
        self.episode_offset_c = 0.0
        self.active_episode_steps = 0

    def next_event(self) -> dict[str, Any]:
        now = datetime.now()
        rng = self.context.rng

        second_of_day = now.hour * 3600 + now.minute * 60 + now.second
        circadian_cycle_c = 0.35 * np.sin(2 * np.pi * second_of_day / 86400 - np.pi / 2)
        noise_c = rng.normal(0, 0.03)
        target_base_c = 36.6 + circadian_cycle_c

        base_temp_c = 0.90 * self.prev_base_temp_c + 0.10 * target_base_c + noise_c

        if self.active_episode_steps == 0 and rng.random() < 0.1:
            self.active_episode_steps = int(rng.integers(8, 20))
            self.episode_offset_c = float(rng.uniform(1.2, 2.4))

        if self.active_episode_steps > 0:
            self.active_episode_steps -= 1
            current_offset_c = self.episode_offset_c
            self.episode_offset_c *= 0.82
            if self.active_episode_steps == 0:
                self.episode_offset_c = 0.0
        else:
            current_offset_c = 0.0

        observed_temp_c = base_temp_c + current_offset_c
        observed_temp_c = float(np.clip(observed_temp_c, 35.8, 40.5))

        self.prev_base_temp_c = base_temp_c

        value = self._convert_from_celsius(observed_temp_c)

        event = self._base_event(now)
        event.update({
            "value": round(value, 2),
            "unit": self.unit,
        })
        return event

    def _convert_from_celsius(self, temp_c: float) -> float:
        if self.unit == "C":
            return temp_c
        return (temp_c * 9 / 5) + 32