from __future__ import annotations

import uuid
from datetime import date
from dataclasses import dataclass

from sqlalchemy.orm import Session

from atmosledger.db.repo.daily_aggregate_repo import DailyAggregateRepo
from atmosledger.db.repo.location_repo import LocationRepo


@dataclass(frozen=True)
class AggregationResult:
    location_id: uuid.UUID
    start_date: date
    end_date: date
    days_upserted: int


class AggregationService:
    def __init__(self, db: Session):
        self._db = db

    def aggregate_daily(
            self,
            *,
            location_id: uuid.UUID,
            start_date: date,
            end_date: date,
    ) -> AggregationResult:
        loc = LocationRepo(self._db).get(location_id)
        if loc is None:
            raise ValueError(f"Location not found: {location_id}")

        days = DailyAggregateRepo(self._db).upsert_from_hourly(
            location_id=location_id,
            start_date=start_date,
            end_date=end_date,
        )

        return AggregationResult(
            location_id=location_id,
            start_date=start_date,
            end_date=end_date,
            days_upserted=days,
        )
