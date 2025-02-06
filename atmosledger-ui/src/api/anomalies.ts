import { apiGet, apiPost } from "./client";
import type { DailyAnomalyPoint, DetectDailyAnomaliesResponse, UUID } from "./types";

export function detectDailyAnomalies(
    locationId: UUID,
    start: string,
    end: string,
    windowDays = 14,
    threshold = 2.5,
    metric = "temperature_2m_mean"
) {
    return apiPost<DetectDailyAnomaliesResponse>(
        `/anomalies/daily/detect?location_id=${locationId}&start=${start}&end=${end}&window_days=${windowDays}&threshold=${threshold}&metric=${encodeURIComponent(metric)}`
    );
}

export function listDailyAnomalies(locationId: UUID, start: string, end: string) {
    return apiGet<DailyAnomalyPoint[]>(
        `/anomalies/daily?location_id=${locationId}&start=${start}&end=${end}`
    );
}
