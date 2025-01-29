from __future__ import annotations

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from atmosledger.db.base import Base
from atmosledger.db.session import get_db
from atmosledger.main import app


def _load_env() -> None:
    """
    Load .env for local test runs. CI should provide env vars explicitly.
    We do not override any already-set env vars.
    """
    repo_root = Path(__file__).resolve().parents[1]
    env_path = repo_root / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)


@pytest.fixture(scope="session")
def test_db_url() -> str:
    _load_env()

    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL must be set for tests. Create a .env file at repo root "
            "or set DATABASE_URL in the environment."
        )
    return url


@pytest.fixture()
def client(test_db_url: str) -> TestClient:
    engine = create_engine(test_db_url, pool_pre_ping=True)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
