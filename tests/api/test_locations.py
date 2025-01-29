from __future__ import annotations


def test_create_location(client):
    payload = {
        "name": "Denver",
        "latitude": 39.7392,
        "longitude": -104.9903,
        "timezone": "America/Denver",
    }

    r = client.post("/locations", json=payload)
    assert r.status_code == 201, r.text
    body = r.json()
    assert "id" in body
    assert body["name"] == "Denver"
    assert body["timezone"] == "America/Denver"
