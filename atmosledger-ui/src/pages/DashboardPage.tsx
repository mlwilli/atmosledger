import { useEffect, useMemo, useState } from "react";
import { DEMO_LOCATION } from "../api/locations";
import { aggregateDaily, getDaily } from "../api/series";
import { detectDailyAnomalies, listDailyAnomalies } from "../api/anomalies";
import type { DailyAnomalyPoint, DailyPoint } from "../api/types";
import { Card } from "../components/Card";
import { DateRange } from "../components/DateRange";
import { LineSeriesChart } from "../components/LineSeriesChart";
import { AnomaliesTable } from "../components/AnomaliesTable";

function iso(d: Date) {
    return d.toISOString().slice(0, 10);
}

export function DashboardPage() {
    const location = DEMO_LOCATION;

    const [start, setStart] = useState("2025-12-01");
    const [end, setEnd] = useState("2025-12-31");

    const [daily, setDaily] = useState<DailyPoint[]>([]);
    const [anomalies, setAnomalies] = useState<DailyAnomalyPoint[]>([]);
    const [loading, setLoading] = useState(false);
    const [msg, setMsg] = useState<string | null>(null);

    const kpis = useMemo(() => {
        if (daily.length === 0) return null;
        const means = daily.map((d) => d.temperature_2m_mean);
        const min = Math.min(...means);
        const max = Math.max(...means);
        const avg = means.reduce((a, b) => a + b, 0) / means.length;
        return { min, max, avg };
    }, [daily]);

    async function refreshAll() {
        setLoading(true);
        setMsg(null);
        try {
            await aggregateDaily(location.id, start, end);
            await detectDailyAnomalies(location.id, start, end, 14, 2.5, "temperature_2m_mean");

            const [d, a] = await Promise.all([
                getDaily(location.id, start, end),
                listDailyAnomalies(location.id, start, end),
            ]);

            setDaily(d);
            setAnomalies(a);
        } catch (e: any) {
            setMsg(e?.message ?? String(e));
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        void refreshAll();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <div style={{ minHeight: "100vh", background: "#f9fafb", color: "#111827" }}>
            <div style={{ maxWidth: 1100, margin: "0 auto", padding: 24, display: "grid", gap: 16 }}>
                <header style={{ display: "flex", justifyContent: "space-between", alignItems: "end", gap: 16, flexWrap: "wrap" }}>
                    <div>
                        <div style={{ fontSize: 22, fontWeight: 700 }}>Atmosphere Ledger</div>
                        <div style={{ fontSize: 15, color: "#6b7280" }}>By Marcus Williams</div>
                        <div style={{ fontSize: 12, color: "#6b7280" }}>
                            Location: {location.name} ({location.timezone})
                        </div>
                    </div>

                    <div style={{ display: "flex", gap: 12, alignItems: "end", flexWrap: "wrap" }}>
                        <DateRange
                            start={start}
                            end={end}
                            onChange={(r) => {
                                setStart(r.start);
                                setEnd(r.end);
                            }}
                        />
                        <button
                            onClick={() => void refreshAll()}
                            disabled={loading}
                            style={{
                                padding: "10px 14px",
                                borderRadius: 10,
                                border: "1px solid #d1d5db",
                                background: loading ? "#f3f4f6" : "#fff",
                                cursor: loading ? "not-allowed" : "pointer",
                                fontWeight: 600,
                            }}
                        >
                            {loading ? "Refreshing…" : "Refresh"}
                        </button>
                    </div>
                </header>

                {msg && (
                    <div style={{ padding: 12, borderRadius: 12, border: "1px solid #fecaca", background: "#fff1f2", color: "#991b1b" }}>
                        {msg}
                    </div>
                )}

                <section style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 12 }}>
                    <Card title="Days loaded">{daily.length}</Card>
                    <Card title="Mean temp (avg)">{kpis ? kpis.avg.toFixed(2) : "—"}</Card>
                    <Card title="Anomalies in range">{anomalies.length}</Card>
                </section>

                <section style={{ display: "grid", gridTemplateColumns: "1fr", gap: 12 }}>
                    <LineSeriesChart data={daily} anomalies={anomalies} />
                    <AnomaliesTable rows={anomalies} />
                </section>

                <footer style={{ fontSize: 12, color: "#6b7280" }}>
                    Demo flow: aggregate → detect → visualize. For repeatable screenshots, inject a spike day in daily_aggregates.
                </footer>
            </div>
        </div>
    );
}
