from __future__ import annotations

import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Float, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from atmosledger.db.base import Base


class DailyAnomaly(Base):
    __tablename__ = "anomalies_daily"
    __table_args__ = (
        UniqueConstraint("location_id", "day", "metric", name="uq_anomaly_location_day_metric"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    location_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    day: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    metric: Mapped[str] = mapped_column(String(64), nullable=False)  # e.g. "temperature_2m_mean"
    value: Mapped[float] = mapped_column(Float, nullable=False)

    baseline_mean: Mapped[float] = mapped_column(Float, nullable=False)
    baseline_stddev: Mapped[float] = mapped_column(Float, nullable=False)
    z_score: Mapped[float] = mapped_column(Float, nullable=False)
    threshold: Mapped[float] = mapped_column(Float, nullable=False)
    direction: Mapped[str] = mapped_column(String(16), nullable=False)  # "high" | "low"

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
