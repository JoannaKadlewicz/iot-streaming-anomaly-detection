from dataclasses import dataclass, field
import numpy as np

@dataclass
class MetricContext:
    account_id: str
    device_id: str
    rng: np.random.Generator = field(default_factory=lambda: np.random.default_rng())
