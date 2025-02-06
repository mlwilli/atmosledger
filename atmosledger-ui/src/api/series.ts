import { apiGet, apiPost } from "./client";
import type { DailyPoint, UUID } from "./types";

export function aggregateDaily(locationId: UUID, start: string, end: string) {
    return apiPost<{ days_upserted: number }>(
        `/series/daily/aggregate?location_id=${locationId}&start=${start}&end=${end}`
    );
}

export function getDaily(locationId: UUID, start: string, end: string) {
    return apiGet<DailyPoint[]>(
        `/series/daily?location_id=${locationId}&start=${start}&end=${end}`
    );
}
