from __future__ import annotations

import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from atmosledger.db.repo.anomaly_daily_repo import DailyAnomalyRepo
from atmosledger.db.session import get_db
from atmosledger.services.anomaly_service import DailyAnomalyService

router = APIRouter(tags=["anomalies"])


class DetectDailyAnomaliesResponse(BaseModel):
    location_id: uuid.UUID
    start_date: date
    end_date: date
    metric: str
    window_days: int
    threshold: float
    anomalies_upserted: int


class DailyAnomalyPoint(BaseModel):
    day: date
    metric: str
    value: float
    baseline_mean: float
    baseline_stddev: float
    z_score: float
    threshold: float
    direction: str


@router.post("/anomalies/daily/detect", response_model=DetectDailyAnomaliesResponse, status_code=status.HTTP_202_ACCEPTED)
def detect_daily(
        location_id: uuid.UUID = Query(...),
        start: date = Query(...),
        end: date = Query(...),
        metric: str = Query("temperature_2m_mean"),
        window_days: int = Query(14, ge=3, le=90),
        threshold: float = Query(2.5, gt=0),
        db: Session = Depends(get_db),
) -> DetectDailyAnomaliesResponse:
    if end < start:
        raise HTTPException(status_code=400, detail="end must be >= start")

    try:
        res = DailyAnomalyService(db).detect(
            location_id=location_id,
            start_date=start,
            end_date=end,
            metric=metric,
            window_days=window_days,
            threshold=threshold,
        )
    except ValueError as exc:
        msg = str(exc)
        code = 404 if "not found" in msg.lower() else 400
        raise HTTPException(status_code=code, detail=msg) from exc

    return DetectDailyAnomaliesResponse(**res.__dict__)


@router.get("/anomalies/daily", response_model=list[DailyAnomalyPoint])
def list_daily_anomalies(
        location_id: uuid.UUID = Query(...),
        start: date = Query(...),
        end: date = Query(...),
        metric: str | None = Query(None),
        db: Session = Depends(get_db),
) -> list[DailyAnomalyPoint]:
    if end < start:
        raise HTTPException(status_code=400, detail="end must be >= start")

    rows = DailyAnomalyRepo(db).list_range(location_id=location_id, start_date=start, end_date=end, metric=metric)
    return [
        DailyAnomalyPoint(
            day=r.day,
            metric=r.metric,
            value=r.value,
            baseline_mean=r.baseline_mean,
            baseline_stddev=r.baseline_stddev,
            z_score=r.z_score,
            threshold=r.threshold,
            direction=r.direction,
        )
        for r in rows
    ]
