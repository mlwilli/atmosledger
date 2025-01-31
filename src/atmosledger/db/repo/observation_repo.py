from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from atmosledger.db.orm.observation import ObservationHourly


class ObservationRepo:
    def __init__(self, db: Session):
        self._db = db

    def upsert_hourly(
            self,
            *,
            location_id: uuid.UUID,
            rows: list[dict],
    ) -> int:
        """
        Idempotent upsert by (location_id, observed_at).
        Returns number of rows attempted (best-effort; Postgres doesn't easily return affected count for upserts
        without extra RETURNING logic).
        """
        if not rows:
            return 0

        values = []
        for r in rows:
            observed_at: datetime = r["observed_at"]
            values.append(
                {
                    "location_id": location_id,
                    "observed_at": observed_at,
                    "temperature_2m": r.get("temperature_2m"),
                    "precipitation": r.get("precipitation"),
                }
            )

        stmt = insert(ObservationHourly).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=["location_id", "observed_at"],
            set_={
                "temperature_2m": stmt.excluded.temperature_2m,
                "precipitation": stmt.excluded.precipitation,
            },
        )

        self._db.execute(stmt)
        self._db.commit()
        return len(values)
