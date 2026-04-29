import numpy as np

from domain.entities import Device
from domain.generators import BaseMetricGenerator, MetricContext, StepsGenerator, BodyTemperatureGenerator, \
    HeartRateGenerator, BloodPressureGenerator
from infrastructure.persistence.models.device import Capability


class DeviceGeneratorFactory:

    def build(self, account_id: int, device: Device) -> list[BaseMetricGenerator]:

        ctx = MetricContext(
            account_id=account_id,
            device_id=device.device_id,
            rng=np.random.default_rng(),
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
