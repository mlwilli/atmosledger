# Atmosphere Ledger

**AtmosLedger** Atmospheric data platform for ingesting, aggregating, and analyzing weather time-series data.  
It provides a clean API, background ingestion workers, and a modern chart-driven UI for exploration. 
Simply put, pulls and detects anomalous weather.

---

## Badges

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Features

- **Ingestion** – Async ingestion from Open-Meteo (hourly observations)
- **Aggregation** – Daily rollups (mean / min / max temperature, precipitation)
- **Anomaly Detection** – Rolling z-score–based daily anomaly detection
- **Scalable Architecture** – FastAPI + PostgreSQL + Redis + RQ workers
- **Tested** – Pytest coverage for core API flows
- **UI Demo** – React + Recharts frontend for visual exploration

---

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy 2.x, Alembic
- PostgreSQL
- Redis + RQ

### Frontend
- React (Vite)
- Recharts

---

## Quick Start (Development)

```bash
# Start infrastructure + worker
docker compose up -d

# Install backend dependencies
poetry install

# Run API
poetry run uvicorn atmosledger.main:app --reload

# FrontEnd

npm install
npm run dev

Example API Endpoints
http

POST /ingestions/open-meteo/run
POST /series/daily/aggregate
GET  /series/daily
POST /anomalies/daily/detect
GET  /anomalies/daily