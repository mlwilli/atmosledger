from __future__ import annotations

from fastapi import FastAPI

from atmosledger.api.routes.health import router as health_router
from atmosledger.api.routes.ingestion import router as ingestion_router
from atmosledger.api.routes.locations import router as locations_router
from atmosledger.logging_config import configure_logging
from atmosledger.settings import settings
from atmosledger.api.routes.series import router as series_router
from atmosledger.api.routes.anomalies import router as anomalies_router
from fastapi.middleware.cors import CORSMiddleware


configure_logging(settings.log_level)

app = FastAPI(title="AtmosLedger", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(locations_router)
app.include_router(ingestion_router)
app.include_router(series_router)
app.include_router(anomalies_router)

