from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from atmosledger.db.session import get_db
from atmosledger.db.repo.location_repo import LocationRepo

router = APIRouter(prefix="/locations", tags=["locations"])


class CreateLocationRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone: str = Field(min_length=1, max_length=64)


class LocationResponse(BaseModel):
    id: uuid.UUID
    name: str
    latitude: float
    longitude: float
    timezone: str


@router.post(
    "",
    response_model=LocationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_location(
        req: CreateLocationRequest,
        db: Session = Depends(get_db),
) -> LocationResponse:
    repo = LocationRepo(db)

    try:
        location = repo.create(
            name=req.name.strip(),
            latitude=req.latitude,
            longitude=req.longitude,
            timezone=req.timezone.strip(),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return LocationResponse(
        id=location.id,
        name=location.name,
        latitude=location.latitude,
        longitude=location.longitude,
        timezone=location.timezone,
    )
