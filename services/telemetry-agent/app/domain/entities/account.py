from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass(frozen=True)
class Account:
    name: str
    account_id: int | None = None
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
