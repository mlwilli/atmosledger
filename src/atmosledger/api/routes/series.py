from __future__ import annotations

import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from atmosledger.db.repo.daily_aggregate_repo import DailyAggregateRepo
from atmosledger.db.session import get_db
from atmosledger.services.aggregation_service import AggregationService

router = APIRouter(tags=["series"])


class AggregateDailyResponse(BaseModel):
    location_id: uuid.UUID
    start_date: date
    end_date: date
    days_upserted: int


class DailyPoint(BaseModel):
    day: date
    temperature_2m_mean: float | None
    temperature_2m_min: float | None
    temperature_2m_max: float | None
    precipitation_sum: float | None


@router.post("/series/daily/aggregate", response_model=AggregateDailyResponse, status_code=status.HTTP_202_ACCEPTED)
def aggregate_daily(
        location_id: uuid.UUID = Query(...),
        start: date = Query(...),
        end: date = Query(...),
        db: Session = Depends(get_db),
) -> AggregateDailyResponse:
    if end < start:
        raise HTTPException(status_code=400, detail="end must be >= start")

    try:
        res = AggregationService(db).aggregate_daily(location_id=location_id, start_date=start, end_date=end)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return AggregateDailyResponse(
        location_id=res.location_id,
        start_date=res.start_date,
        end_date=res.end_date,
        days_upserted=res.days_upserted,
    )


@router.get("/series/daily", response_model=list[DailyPoint])
def get_daily_series(
        location_id: uuid.UUID = Query(...),
        start: date = Query(...),
        end: date = Query(...),
        db: Session = Depends(get_db),
) -> list[DailyPoint]:
    if end < start:
        raise HTTPException(status_code=400, detail="end must be >= start")

    rows = DailyAggregateRepo(db).list_range(location_id=location_id, start_date=start, end_date=end)
    return [
        DailyPoint(
            day=r.day,
            temperature_2m_mean=r.temperature_2m_mean,
            temperature_2m_min=r.temperature_2m_min,
            temperature_2m_max=r.temperature_2m_max,
            precipitation_sum=r.precipitation_sum,
        )
        for r in rows
    ]
