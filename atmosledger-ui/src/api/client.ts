export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL as string;

export async function apiGet<T>(path: string): Promise<T> {
    const res = await fetch(`${API_BASE_URL}${path}`);
    if (!res.ok) {
        const txt = await res.text();
        throw new Error(`GET ${path} failed: ${res.status} ${txt}`);
    }
    return (await res.json()) as T;
}

export async function apiPost<T>(path: string): Promise<T> {
    const res = await fetch(`${API_BASE_URL}${path}`, { method: "POST" });
    if (!res.ok) {
        const txt = await res.text();
        throw new Error(`POST ${path} failed: ${res.status} ${txt}`);
    }
    return (await res.json()) as T;
}
