from dataclasses import dataclass, field
from enum import Enum

import numpy as np


class ActivityLevel(Enum):
    SLEEPING = "sleeping"
    RESTING = "resting"
    WALKING = "walking"
    RUNNING = "running"
    WORKOUT = "workout"


@dataclass
class UserActivityState:
    level: ActivityLevel = ActivityLevel.RESTING
    steps_remaining_in_burst: int = 0

    def transition(self, rng: np.random.Generator, hour: int) -> None:
        weights = _activity_weights_by_hour(hour)
        self.level = rng.choice(list(ActivityLevel), p=weights)


@dataclass
class MetricContext:
    account_id: int
    device_id: int
    rng: np.random.Generator = field(default_factory=lambda: np.random.default_rng())
    activity: UserActivityState = field(default_factory=UserActivityState)


def _activity_weights_by_hour(hour: int) -> list[float]:
    # [SLEEPING, RESTING, WALKING, RUNNING, WORKOUT]
    if 0 <= hour < 6:
        return [0.95, 0.04, 0.01, 0.00, 0.00]
    elif 6 <= hour < 8:      # poranek — wstawanie, śniadanie
        return [0.05, 0.68, 0.20, 0.04, 0.03]
    elif 8 <= hour < 12:     # praca
        return [0.00, 0.83, 0.12, 0.01, 0.04]
    elif 12 <= hour < 14:    # lunch — krótki spacer
        return [0.00, 0.68, 0.22, 0.02, 0.08]
    elif 14 <= hour < 17:    # praca
        return [0.00, 0.87, 0.10, 0.01, 0.02]
    elif 17 <= hour < 20:    # po pracy — główne okno aktywności
        return [0.00, 0.52, 0.24, 0.08, 0.16]
    elif 20 <= hour < 22:    # wieczór
        return [0.00, 0.75, 0.20, 0.02, 0.03]
    else:                    # 22-24 zasypianie
        return [0.55, 0.38, 0.06, 0.00, 0.01]