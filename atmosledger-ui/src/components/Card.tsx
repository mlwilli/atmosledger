import type { ReactNode } from "react";

export function Card(props: { title: string; children: ReactNode }) {
    return (
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 16, background: "#fff" }}>
            <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 8 }}>{props.title}</div>
            <div style={{ fontSize: 18 }}>{props.children}</div>
        </div>
    );
}
