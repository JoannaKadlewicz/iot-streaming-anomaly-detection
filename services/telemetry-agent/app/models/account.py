from datetime import datetime


class Account:

    def __init__(self, name, created_at: datetime | None = None, is_active: bool | None = None):
        self.name = name
        self.created_at = created_at if created_at is not None else datetime.now()
        self.is_active = is_active if is_active is not None else True
