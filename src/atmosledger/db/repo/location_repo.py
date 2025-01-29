from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from atmosledger.db.orm.location import Location


class LocationRepo:
    def __init__(self, db: Session):
        self._db = db

    def create(self, name: str, latitude: float, longitude: float, timezone: str) -> Location:
        if not name:
            raise ValueError("name must not be blank")
        if not timezone:
            raise ValueError("timezone must not be blank")

        loc = Location(name=name, latitude=latitude, longitude=longitude, timezone=timezone)
        self._db.add(loc)
        self._db.commit()
        self._db.refresh(loc)
        return loc

    def get(self, location_id) -> Location | None:
        stmt = select(Location).where(Location.id == location_id)
        return self._db.execute(stmt).scalars().first()
