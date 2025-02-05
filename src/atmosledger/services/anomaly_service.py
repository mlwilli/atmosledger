from __future__ import annotations

import math
import uuid
from dataclasses import dataclass
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from atmosledger.db.orm.daily_aggregate import DailyAggregate
from atmosledger.db.repo.anomaly_daily_repo import DailyAnomalyRepo
from atmosledger.db.repo.location_repo import LocationRepo


@dataclass(frozen=True)
class DetectDailyAnomaliesResult:
    location_id: uuid.UUID
    start_date: date
    end_date: date
    metric: str
    window_days: int
    threshold: float
    anomalies_upserted: int


class DailyAnomalyService:
    def __init__(self, db: Session):
        self._db = db

    def detect(
            self,
            *,
            location_id: uuid.UUID,
            start_date: date,
            end_date: date,
            metric: str = "temperature_2m_mean",
            window_days: int = 14,
            threshold: float = 2.5,
    ) -> DetectDailyAnomaliesResult:
        loc = LocationRepo(self._db).get(location_id)
        if loc is None:
            raise ValueError(f"Location not found: {location_id}")

        if window_days < 3:
            raise ValueError("window_days must be >= 3")
        if threshold <= 0:
            raise ValueError("threshold must be > 0")

        stmt = (
            select(DailyAggregate)
            .where(DailyAggregate.location_id == location_id)
            .where(DailyAggregate.day <= end_date)
            .order_by(DailyAggregate.day.asc())
        )
        rows = list(self._db.execute(stmt).scalars().all())

        series: list[tuple[date, float]] = []
        for r in rows:
            v = getattr(r, metric, None)
            if v is None:
                continue
            series.append((r.day, float(v)))

        if not series:
            return DetectDailyAnomaliesResult(
                location_id=location_id,
                start_date=start_date,
                end_date=end_date,
                metric=metric,
                window_days=window_days,
                threshold=threshold,
                anomalies_upserted=0,
            )

        values = [v for _, v in series]

        anomalies: list[dict] = []
        for i, (day, value) in enumerate(series):
            if day < start_date or day > end_date:
                continue

            window = values[max(0, i - window_days) : i]  # prior points only
            if len(window) < window_days:
                continue

            mean = sum(window) / len(window)
            var = sum((x - mean) ** 2 for x in window) / len(window)
            std = math.sqrt(var)
            if std == 0:
                continue

            z = (value - mean) / std
            if abs(z) >= threshold:
                anomalies.append(
                    {
                        "id": uuid.uuid4(),
                        "location_id": location_id,
                        "day": day,
                        "metric": metric,
                        "value": value,
                        "baseline_mean": mean,
                        "baseline_stddev": std,
                        "z_score": z,
                        "threshold": threshold,
                        "direction": "high" if z > 0 else "low",
                    }
                )

        upserted = DailyAnomalyRepo(self._db).upsert_many(anomalies)

        return DetectDailyAnomaliesResult(
            location_id=location_id,
            start_date=start_date,
            end_date=end_date,
            metric=metric,
            window_days=window_days,
            threshold=threshold,
            anomalies_upserted=upserted,
        )
