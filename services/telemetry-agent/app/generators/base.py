from datetime import datetime
from typing import Any
from uuid import uuid4

from generators.context import MetricContext


class BaseMetricGenerator:
    metric_type: str
    unit: str

    def __init__(self, context: MetricContext) -> None:
        self.context = context

    def next_event(self) -> dict[str, Any]:
        raise NotImplementedError

    def _base_event(self, event_ts: datetime) -> dict[str, Any]:
        return {
            "event_id": str(uuid4()),
            "account_id": self.context.account_id,
            "device_id": self.context.device_id,
            "metric_type": self.metric_type,
            "event_ts": event_ts.isoformat(),
        }
