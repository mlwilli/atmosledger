export type UUID = string;

export type Location = {
    id: UUID;
    name: string;
    latitude: number;
    longitude: number;
    timezone: string;
};

export type DailyPoint = {
    day: string; // YYYY-MM-DD
    temperature_2m_mean: number;
    temperature_2m_min: number;
    temperature_2m_max: number;
    precipitation_sum: number;
};

export type DetectDailyAnomaliesResponse = {
    location_id: UUID;
    start_date: string;
    end_date: string;
    metric: string;
    window_days: number;
    threshold: number;
    anomalies_upserted: number;
};

export type DailyAnomalyPoint = {
    day: string;
    metric: string;
    value: number;
    baseline_mean: number;
    baseline_stddev: number;
    z_score: number;
    threshold: number;
    direction: "high" | "low";
};
