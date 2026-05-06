from dataclasses import dataclass, field
from enum import Enum

import numpy as np


class ActivityLevel(Enum):
    SLEEPING = "sleeping"
    RESTING = "resting"
    WALKING = "walking"
    RUNNING = "running"
    WORKOUT = "workout"

class ActivityProfile(Enum):
    SEDENTARY = "sedentary"
    NORMAL = "normal"
    ACTIVE = "active"

@dataclass
class UserActivityState:
    level: ActivityLevel = ActivityLevel.RESTING
    profile: ActivityProfile = ActivityProfile.SEDENTARY

    def transition(self, rng: np.random.Generator, hour: int) -> None:
        weights = _activity_weights_by_hour(hour, self.profile)
        self.level = rng.choice(list(ActivityLevel), p=weights)


@dataclass
class MetricContext:
    account_id: int
    device_id: int
    rng: np.random.Generator = field(default_factory=lambda: np.random.default_rng())
    activity: UserActivityState = field(default_factory=UserActivityState)




_WEIGHTS: dict[ActivityProfile, list[list[float]]] = {
    ActivityProfile.SEDENTARY: [
        [0.95, 0.04, 0.01, 0.00, 0.00],  # 0-6
        [0.05, 0.88, 0.06, 0.00, 0.01],  # 6-8
        [0.00, 0.95, 0.04, 0.00, 0.01],  # 8-12
        [0.00, 0.90, 0.07, 0.00, 0.03],  # 12-14
        [0.00, 0.96, 0.03, 0.00, 0.01],  # 14-17
        [0.00, 0.82, 0.12, 0.01, 0.05],  # 17-20
        [0.00, 0.90, 0.08, 0.00, 0.02],  # 20-22
        [0.55, 0.42, 0.03, 0.00, 0.00],  # 22-24
    ],
    ActivityProfile.NORMAL: [
        [0.95, 0.04, 0.01, 0.00, 0.00],  # 0-6
        [0.05, 0.68, 0.20, 0.04, 0.03],  # 6-8
        [0.00, 0.83, 0.12, 0.01, 0.04],  # 8-12
        [0.00, 0.68, 0.22, 0.02, 0.08],  # 12-14
        [0.00, 0.87, 0.10, 0.01, 0.02],  # 14-17
        [0.00, 0.52, 0.24, 0.08, 0.16],  # 17-20
        [0.00, 0.75, 0.20, 0.02, 0.03],  # 20-22
        [0.55, 0.38, 0.06, 0.00, 0.01],  # 22-24
    ],
    ActivityProfile.ACTIVE: [
        [0.90, 0.08, 0.02, 0.00, 0.00],  # 0-6
        [0.02, 0.45, 0.30, 0.15, 0.08],  # 6-8
        [0.00, 0.72, 0.18, 0.03, 0.07],  # 8-12
        [0.00, 0.52, 0.30, 0.05, 0.13],  # 12-14
        [0.00, 0.75, 0.15, 0.03, 0.07],  # 14-17
        [0.00, 0.30, 0.30, 0.15, 0.25],  # 17-20
        [0.00, 0.62, 0.28, 0.05, 0.05],  # 20-22
        [0.50, 0.42, 0.07, 0.00, 0.01],  # 22-24
    ],
}

_HOUR_SLOTS = [6, 8, 12, 14, 17, 20, 22, 24]


def _activity_weights_by_hour(hour: int, profile: ActivityProfile) -> list[float]:
    slot = next((i for i, h in enumerate(_HOUR_SLOTS) if hour < h), len(_HOUR_SLOTS) - 1)
    return _WEIGHTS[profile][slot]