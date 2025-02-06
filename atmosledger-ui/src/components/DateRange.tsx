export function DateRange(props: {
    start: string;
    end: string;
    onChange: (next: { start: string; end: string }) => void;
}) {
    return (
        <div style={{ display: "flex", gap: 12, alignItems: "end", flexWrap: "wrap" }}>
            <label style={{ display: "grid", gap: 6, fontSize: 12, color: "#374151" }}>
                Start
                <input
                    type="date"
                    value={props.start}
                    onChange={(e) => props.onChange({ start: e.target.value, end: props.end })}
                    style={{ padding: 8, borderRadius: 8, border: "1px solid #d1d5db" }}
                />
            </label>
            <label style={{ display: "grid", gap: 6, fontSize: 12, color: "#374151" }}>
                End
                <input
                    type="date"
                    value={props.end}
                    onChange={(e) => props.onChange({ start: props.start, end: e.target.value })}
                    style={{ padding: 8, borderRadius: 8, border: "1px solid #d1d5db" }}
                />
            </label>
        </div>
    );
}
