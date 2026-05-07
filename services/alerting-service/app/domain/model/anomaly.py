from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Anomaly:
    account_id: int
    device_id: int
    metric: str
    window_start: datetime
    window_end: datetime
    anomaly_reason: str
    alert_sent: bool
