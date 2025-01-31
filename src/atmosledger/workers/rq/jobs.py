from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy.orm import Session

from atmosledger.db.session import SessionLocal
from atmosledger.providers.open_meteo_client import OpenMeteoClient
from atmosledger.services.ingestion_service import IngestionService
from atmosledger.settings import settings


def ingest_open_meteo_hourly_job(location_id: str, start_date: str, end_date: str) -> dict:
    """
    RQ job entrypoint. Args are strings for serialization.
    """
    loc_id = uuid.UUID(location_id)
    sd = date.fromisoformat(start_date)
    ed = date.fromisoformat(end_date)

    db: Session = SessionLocal()
    try:
        client = OpenMeteoClient(settings.open_meteo_archive_base_url)
        svc = IngestionService(db, client)
        result = svc.ingest_open_meteo_hourly(location_id=loc_id, start_date=sd, end_date=ed)
        return {
            "location_id": str(result.location_id),
            "start_date": result.start_date.isoformat(),
            "end_date": result.end_date.isoformat(),
            "rows_upserted": result.rows_upserted,
        }
    finally:
        db.close()
