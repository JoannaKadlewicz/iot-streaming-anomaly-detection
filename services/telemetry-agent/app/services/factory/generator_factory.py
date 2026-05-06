import random

import numpy as np

from domain.generators import BaseMetricGenerator, MetricContext, StepsGenerator, BodyTemperatureGenerator, \
    HeartRateGenerator, BloodPressureGenerator
from domain.generators.context import ActivityProfile, UserActivityState
from domain.model import Device
from domain.model.device import Capability


class DeviceGeneratorFactory:


    def build(self, account_id: int, device: Device) -> list[BaseMetricGenerator]:
        _PROFILE_DISTRIBUTION: list[tuple[ActivityProfile, float]] = [
            (ActivityProfile.SEDENTARY, 0.33),
            (ActivityProfile.NORMAL, 0.45),
            (ActivityProfile.ACTIVE, 0.20),
        ]

        profile = random.choices(
            [p for p, _ in _PROFILE_DISTRIBUTION],
            weights=[w for _, w in _PROFILE_DISTRIBUTION],
        )[0]

        ctx = MetricContext(
            account_id=account_id,
            device_id=device.device_id,
            rng=np.random.default_rng(),
            activity=UserActivityState(profile=profile),
        )
        return [self._create(capability, ctx) for capability in device.capabilities]

    def _create(self, capability: Capability, ctx: MetricContext) -> BaseMetricGenerator:
        match capability:
            case Capability.STEPS:
                return StepsGenerator(ctx)
            case Capability.TEMPERATURE:
                return BodyTemperatureGenerator(ctx)
            case Capability.HEART_RATE:
                return HeartRateGenerator(ctx)
            case Capability.BLOOD_PRESSURE:
                return BloodPressureGenerator(ctx)
            case _:
                raise ValueError(f"Unknown capability: {capability}")
