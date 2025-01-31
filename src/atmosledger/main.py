from __future__ import annotations

from fastapi import FastAPI

from atmosledger.api.routes.health import router as health_router
from atmosledger.api.routes.ingestion import router as ingestion_router
from atmosledger.api.routes.locations import router as locations_router
from atmosledger.logging_config import configure_logging
from atmosledger.settings import settings

configure_logging(settings.log_level)

app = FastAPI(title="AtmosLedger", version="0.1.0")

app.include_router(health_router)
app.include_router(locations_router)
app.include_router(ingestion_router)
