$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"
poetry run uvicorn atmosledger.main:app --reload
