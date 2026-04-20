from datetime import datetime
from enum import Enum

from sqlalchemy import String, Enum as SqlEnum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import mapped_column, Mapped

from entities.base import Base


class DeviceType(str, Enum):
    WATCH = "smartwatch"
    BAND = "smart band"
    RING = "smart ring"


class Capability(str, Enum):
    STEPS = "steps"
    TEMPERATURE = "temperature"
    HEART_RATE = "heart_rate"
    BLOOD_PRESSURE = "blood_pressure"


class DeviceEntity(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.account_id"), nullable=False)
    device_type: Mapped[DeviceType] = mapped_column(SqlEnum(DeviceType, name="device_type", values_callable=lambda enum_cls: [e.value for e in enum_cls],))
    capabilities: Mapped[list[Capability]] = mapped_column(ARRAY(SqlEnum(Capability, values_callable=lambda enum_cls: [e.value for e in enum_cls],)), default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())