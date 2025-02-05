from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from atmosledger.db.orm.anomaly_daily import DailyAnomaly


class DailyAnomalyRepo:
    def __init__(self, db: Session):
        self._db = db

    def upsert_many(self, rows: list[dict]) -> int:
        if not rows:
            return 0

        stmt = insert(DailyAnomaly).values(rows)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_anomaly_location_day_metric",
            set_={
                "value": stmt.excluded.value,
                "baseline_mean": stmt.excluded.baseline_mean,
                "baseline_stddev": stmt.excluded.baseline_stddev,
                "z_score": stmt.excluded.z_score,
                "threshold": stmt.excluded.threshold,
                "direction": stmt.excluded.direction,
            },
        )
        self._db.execute(stmt)
        self._db.commit()
        return len(rows)

    def list_range(
            self,
            *,
            location_id: uuid.UUID,
            start_date: date,
            end_date: date,
            metric: str | None = None,
    ) -> list[DailyAnomaly]:
        stmt = (
            select(DailyAnomaly)
            .where(DailyAnomaly.location_id == location_id)
            .where(DailyAnomaly.day.between(start_date, end_date))
            .order_by(DailyAnomaly.day.asc())
        )
        if metric:
            stmt = stmt.where(DailyAnomaly.metric == metric)
        return list(self._db.execute(stmt).scalars().all())
