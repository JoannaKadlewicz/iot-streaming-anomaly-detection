from typing import Callable

from pyspark.sql import DataFrame

from domain.transformations.silver import heart_rate, steps, temperature, blood_pressure

TransformFn = Callable[[DataFrame], DataFrame]

METRICS_TRANSFORMS: dict[str, TransformFn] = {
    "heart_rate": heart_rate.transform,
    "steps": steps.transform,
    "temperature": temperature.transform,
    "blood_pressure": blood_pressure.transform,
}


def get_function(metric_type: str) -> TransformFn:
    fn: TransformFn = METRICS_TRANSFORMS[metric_type]
    if fn is None:
        raise ValueError(f"Unknown metric type {metric_type}")
    return fn


def supported_metrics() -> list[str]:
    return list(METRICS_TRANSFORMS.keys())
