from __future__ import annotations

import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Float, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from atmosledger.db.base import Base


class DailyAggregate(Base):
    __tablename__ = "daily_aggregates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("locations.id", ondelete="CASCADE"), nullable=False
    )

    day: Mapped[date] = mapped_column(Date, nullable=False)

    temperature_2m_mean: Mapped[float | None] = mapped_column(Float, nullable=True)
    temperature_2m_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    temperature_2m_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    precipitation_sum: Mapped[float | None] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )


Index("ix_daily_agg_location_day", DailyAggregate.location_id, DailyAggregate.day, unique=True)
