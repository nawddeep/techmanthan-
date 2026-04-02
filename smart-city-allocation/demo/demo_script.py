#!/usr/bin/env python3
"""
End-to-end smoke test of the Smart City API.
Usage: from repo root `python demo/demo_script.py`
Requires: backend running (default http://127.0.0.1:8000), admin credentials.
"""
import json
import os
import sys

import requests

BASE = os.environ.get("API_URL", "http://127.0.0.1:8000").rstrip("/")
USER = os.environ.get("API_USER", "admin")
PASSWORD = os.environ.get("API_PASSWORD", "admin123")


def main() -> int:
    r = requests.post(
        f"{BASE}/auth/token",
        data={"username": USER, "password": PASSWORD},
        timeout=30,
    )
    if r.status_code != 200:
        print("Auth failed:", r.status_code, r.text)
        return 1
    token = r.json()["access_token"]
    h = {"Authorization": f"Bearer {token}"}

    endpoints = [
        ("GET", "/health", None),
        ("GET", "/system/decision", None),
        ("GET", "/map-data", None),
        ("GET", "/history/trends", None),
        ("GET", "/models/stats", None),
        (
            "POST",
            "/predict/traffic",
            {
                "hour": 14,
                "day_enc": 3,
                "junction_enc": 2,
                "weather_enc": 0,
                "vehicles": 200,
            },
        ),
        (
            "POST",
            "/predict/waste",
            {
                "area": 2,
                "day_of_week": 3,
                "population_density": 3000,
                "last_collection_days": 4,
                "bin_fill_pct": 65,
            },
        ),
    ]

    for method, path, body in endpoints:
        url = f"{BASE}{path}"
        if method == "GET":
            resp = requests.get(url, headers=h, timeout=60)
        else:
            resp = requests.post(url, headers=h, json=body, timeout=60)
        print(f"\n=== {method} {path} -> {resp.status_code} ===")
        try:
            print(json.dumps(resp.json(), indent=2)[:2000])
        except Exception:
            print(resp.text[:500])

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
