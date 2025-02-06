import type { DailyAnomalyPoint } from "../api/types";

export function AnomaliesTable(props: { rows: DailyAnomalyPoint[] }) {
    if (props.rows.length === 0) {
        return (
            <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 16, background: "#fff" }}>
                <div style={{ fontSize: 14 }}>Anomalies</div>
                <div style={{ marginTop: 8, color: "#6b7280" }}>No anomalies in range.</div>
            </div>
        );
    }

    return (
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 16, background: "#fff" }}>
            <div style={{ fontSize: 14, marginBottom: 8 }}>Anomalies</div>
            <div style={{ overflowX: "auto" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
                    <thead>
                    <tr style={{ textAlign: "left", borderBottom: "1px solid #e5e7eb" }}>
                        <th style={{ padding: 8 }}>Day</th>
                        <th style={{ padding: 8 }}>Metric</th>
                        <th style={{ padding: 8 }}>Value</th>
                        <th style={{ padding: 8 }}>Z</th>
                        <th style={{ padding: 8 }}>Direction</th>
                    </tr>
                    </thead>
                    <tbody>
                    {props.rows.map((r) => (
                        <tr key={`${r.day}-${r.metric}`} style={{ borderBottom: "1px solid #f3f4f6" }}>
                            <td style={{ padding: 8 }}>{r.day}</td>
                            <td style={{ padding: 8 }}>{r.metric}</td>
                            <td style={{ padding: 8 }}>{r.value.toFixed(3)}</td>
                            <td style={{ padding: 8 }}>{r.z_score.toFixed(2)}</td>
                            <td style={{ padding: 8 }}>{r.direction}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
