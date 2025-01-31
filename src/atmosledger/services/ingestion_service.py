from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from sqlalchemy.orm import Session

from atmosledger.db.repo.location_repo import LocationRepo
from atmosledger.db.repo.observation_repo import ObservationRepo
from atmosledger.providers.open_meteo_client import OpenMeteoClient


@dataclass(frozen=True)
class IngestionResult:
    location_id: uuid.UUID
    start_date: date
    end_date: date
    rows_upserted: int


class IngestionService:
    def __init__(self, db: Session, open_meteo: OpenMeteoClient):
        self._db = db
        self._open_meteo = open_meteo

    def ingest_open_meteo_hourly(
            self,
            *,
            location_id: uuid.UUID,
            start_date: date,
            end_date: date,
    ) -> IngestionResult:
        loc = LocationRepo(self._db).get(location_id)
        if loc is None:
            raise ValueError(f"Location not found: {location_id}")

        series = self._open_meteo.fetch_archive_hourly(
            latitude=loc.latitude,
            longitude=loc.longitude,
            timezone=loc.timezone,
            start_date=start_date,
            end_date=end_date,
        )

        # Map to DB rows. Open-Meteo hourly.time is ISO strings in the requested timezone.
        # Python 3.12: datetime.fromisoformat handles "YYYY-MM-DDTHH:MM".
        rows: list[dict] = []
        for i, t in enumerate(series.time):
            observed_at = datetime.fromisoformat(t)
            rows.append(
                {
                    "observed_at": observed_at,
                    "temperature_2m": _safe_get(series.temperature_2m, i),
                    "precipitation": _safe_get(series.precipitation, i),
                }
            )

        upserted = ObservationRepo(self._db).upsert_hourly(location_id=loc.id, rows=rows)
        return IngestionResult(
            location_id=loc.id,
            start_date=start_date,
            end_date=end_date,
            rows_upserted=upserted,
        )


def _safe_get(arr: Optional[list], idx: int):
    if arr is None:
        return None
    if idx >= len(arr):
        return None
    return arr[idx]
