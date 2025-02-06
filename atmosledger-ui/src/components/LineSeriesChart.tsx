import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceDot } from "recharts";
import type { DailyPoint, DailyAnomalyPoint } from "../api/types";

export function LineSeriesChart(props: {
    data: DailyPoint[];
    anomalies: DailyAnomalyPoint[];
}) {
    const anomalyDays = new Set(props.anomalies.map((a) => a.day));

    const chartData = props.data.map((d) => ({
        ...d,
        anomaly: anomalyDays.has(d.day) ? d.temperature_2m_mean : null,
    }));

    return (
        <div style={{ height: 360, border: "1px solid #e5e7eb", borderRadius: 12, padding: 12, background: "#fff" }}>
            <div style={{ fontSize: 14, marginBottom: 8 }}>Temperature (daily mean) with anomaly markers</div>
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="day" tick={{ fontSize: 12 }} />
                    <YAxis tick={{ fontSize: 12 }} />
                    <Tooltip />
                    <Line type="monotone" dataKey="temperature_2m_mean" dot={false} />
                    {chartData
                        .filter((d) => d.anomaly !== null)
                        .map((d) => (
                            <ReferenceDot key={d.day} x={d.day} y={d.temperature_2m_mean} r={6} />
                        ))}
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
