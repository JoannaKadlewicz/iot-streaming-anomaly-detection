from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass(frozen=True)
class Account:
    account_id: int
    name: str
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
