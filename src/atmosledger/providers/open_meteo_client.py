from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

import httpx


@dataclass(frozen=True)
class OpenMeteoHourlySeries:
    time: list[str]
    temperature_2m: list[float] | None
    precipitation: list[float] | None


class OpenMeteoClient:
    """
    Uses Open-Meteo archive API for historical hourly data.
    Endpoint: /v1/archive
    """

    def __init__(self, archive_base_url: str, timeout_s: float = 20.0):
        self._base = archive_base_url.rstrip("/")
        self._timeout = timeout_s

    def fetch_archive_hourly(
            self,
            *,
            latitude: float,
            longitude: float,
            timezone: str,
            start_date: date,
            end_date: date,
    ) -> OpenMeteoHourlySeries:
        url = f"{self._base}/archive"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "timezone": timezone,
            # We store only these for v1:
            "hourly": "temperature_2m,precipitation",
        }

        with httpx.Client(timeout=self._timeout) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            data: dict[str, Any] = resp.json()

        hourly = data.get("hourly") or {}
        time = hourly.get("time") or []
        temperature = hourly.get("temperature_2m")
        precipitation = hourly.get("precipitation")

        if not isinstance(time, list) or len(time) == 0:
            raise ValueError("Open-Meteo response missing hourly.time")

        return OpenMeteoHourlySeries(
            time=time,
            temperature_2m=temperature if isinstance(temperature, list) else None,
            precipitation=precipitation if isinstance(precipitation, list) else None,
        )
