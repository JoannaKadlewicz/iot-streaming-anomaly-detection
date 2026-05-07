from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Anomaly:
    anomaly_id: UUID
    account_id: int
    device_id: int
    metric: str
    window_start: datetime
    window_end: datetime
    anomaly_reason: str
    alert_sent: bool
