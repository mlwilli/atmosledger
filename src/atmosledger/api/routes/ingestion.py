from __future__ import annotations

import uuid
from datetime import date

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from redis import Redis
from rq import Queue

from atmosledger.settings import settings
from atmosledger.workers.rq.jobs import ingest_open_meteo_hourly_job

router = APIRouter(prefix="/ingestions/open-meteo", tags=["ingestion"])


class EnqueueIngestionResponse(BaseModel):
    job_id: str
    location_id: uuid.UUID
    start_date: date
    end_date: date


@router.post("/run", response_model=EnqueueIngestionResponse, status_code=status.HTTP_202_ACCEPTED)
def enqueue_open_meteo_ingestion(
        location_id: uuid.UUID = Query(..., description="Location UUID"),
        start: date = Query(..., description="Start date (YYYY-MM-DD)"),
        end: date = Query(..., description="End date (YYYY-MM-DD)"),
) -> EnqueueIngestionResponse:
    if end < start:
        raise HTTPException(status_code=400, detail="end must be >= start")

    redis_conn = Redis.from_url(settings.redis_url)
    queue = Queue(settings.rq_queue, connection=redis_conn)

    job = queue.enqueue(
        ingest_open_meteo_hourly_job,
        str(location_id),
        start.isoformat(),
        end.isoformat(),
        job_timeout=300,
        result_ttl=3600,
        failure_ttl=3600,
    )

    return EnqueueIngestionResponse(
        job_id=job.id,
        location_id=location_id,
        start_date=start,
        end_date=end,
    )
