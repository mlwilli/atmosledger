from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import bindparam, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from atmosledger.db.orm.daily_aggregate import DailyAggregate


class DailyAggregateRepo:
    def __init__(self, db: Session):
        self._db = db

    def upsert_from_hourly(
            self,
            *,
            location_id: uuid.UUID,
            start_date: date,
            end_date: date,
    ) -> int:
        """
        Aggregates observations_hourly into daily_aggregates for [start_date, end_date].
        Uses SQL aggregation for correctness and speed.
        """

        sql = (
            text(
                """
                SELECT
                    CAST(:location_id AS uuid) AS location_id,
                    (timezone('UTC', observed_at))::date AS day,
                  AVG(temperature_2m) AS temperature_2m_mean,
                  MIN(temperature_2m) AS temperature_2m_min,
                  MAX(temperature_2m) AS temperature_2m_max,
                  SUM(precipitation) AS precipitation_sum
                FROM observations_hourly
                WHERE location_id = CAST(:location_id AS uuid)
                  AND (timezone('UTC', observed_at))::date BETWEEN :start_date AND :end_date
                GROUP BY (timezone('UTC', observed_at))::date
                ORDER BY day
                """
            )
            .bindparams(
                bindparam("location_id"),
                bindparam("start_date"),
                bindparam("end_date"),
            )
        )

        rows = (
            self._db.execute(
                sql,
                {
                    "location_id": str(location_id),
                    "start_date": start_date,
                    "end_date": end_date,
                },
            )
            .mappings()
            .all()
        )

        if not rows:
            return 0

        stmt = insert(DailyAggregate).values([dict(r) for r in rows])
        stmt = stmt.on_conflict_do_update(
            index_elements=["location_id", "day"],
            set_={
                "temperature_2m_mean": stmt.excluded.temperature_2m_mean,
                "temperature_2m_min": stmt.excluded.temperature_2m_min,
                "temperature_2m_max": stmt.excluded.temperature_2m_max,
                "precipitation_sum": stmt.excluded.precipitation_sum,
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
    ) -> list[DailyAggregate]:
        from sqlalchemy import select

        stmt = (
            select(DailyAggregate)
            .where(DailyAggregate.location_id == location_id)
            .where(DailyAggregate.day.between(start_date, end_date))
            .order_by(DailyAggregate.day.asc())
        )
        return list(self._db.execute(stmt).scalars().all())
