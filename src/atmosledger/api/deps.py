from __future__ import annotations

from collections.abc import Generator

from sqlalchemy.orm import Session

from atmosledger.db.session import get_db


def db_session() -> Generator[Session, None, None]:
    yield from get_db()
