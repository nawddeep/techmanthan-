"""
Real-data-driven city simulation with graceful fallback to statistical simulation.
Exposes get_current_state() with a stable contract for decision_engine and map_data.
"""
from __future__ import annotations

import asyncio
import math
import os
import random
from collections import deque
from datetime import datetime
from typing import Any, Deque, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from api.models.schemas import EmergencySeverity, EmergencyEvent, EventType

# --- Paths ---
_BASE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
_DATA_DIR = os.path.join(_BASE, "data")


def _safe_read_csv(name: str) -> Optional[pd.DataFrame]:
    path = os.path.join(_DATA_DIR, name)
    if not os.path.isfile(path):
        return None
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"[simulation] Failed to read {path}: {e}")
        return None


class RealDataSimulator:
    """
    Samples from real CSV rows, hour-weighted for traffic, progression-aware for waste,
    rolling windows of 50 samples per location, 10 city zones.
    """

    WINDOW = 50
    N_LOC = 10

    def __init__(self, traffic: pd.DataFrame, waste: pd.DataFrame, emergency: pd.DataFrame):
        self.traffic = traffic.copy()
        self.waste = waste.copy()
        self.emergency = emergency.copy()

        self._t_min = float(self.traffic["congestion_score"].min())
        self._t_max = float(self.traffic["congestion_score"].max())
        self._rng = random.Random(42)

        # Per-location rolling buffers of row indices into traffic/waste subsets
        self._traffic_windows: Dict[int, Deque[int]] = {
            i: deque(maxlen=self.WINDOW) for i in range(1, self.N_LOC + 1)
        }
        self._waste_windows: Dict[int, Deque[int]] = {
            i: deque(maxlen=self.WINDOW) for i in range(1, self.N_LOC + 1)
        }

        # Junction id in clean data is 0..7 — map location 1..10
        self._loc_to_junction = {i: (i - 1) % 8 for i in range(1, self.N_LOC + 1)}
        self._loc_to_area = {i: (i - 1) % 8 for i in range(1, self.N_LOC + 1)}
        self._loc_to_zone = {i: (i - 1) % 5 for i in range(1, self.N_LOC + 1)}  # emergency zones 0-4

        self._traffic_idx: Dict[int, np.ndarray] = {}
        for loc, junc in self._loc_to_junction.items():
            mask = self.traffic["junction"].values == junc
            idx = np.flatnonzero(mask)
            if len(idx) == 0:
                idx = np.arange(len(self.traffic))
            self._traffic_idx[loc] = idx

        self._waste_idx: Dict[int, np.ndarray] = {}
        for loc, area in self._loc_to_area.items():
            mask = self.waste["area"].values == area
            idx = np.flatnonzero(mask)
            if len(idx) == 0:
                idx = np.arange(len(self.waste))
            self._waste_idx[loc] = idx

        # Observed fill deltas per area for realistic progression
        self._fill_delta_by_area: Dict[int, List[float]] = {}
        for area in range(8):
            sub = self.waste[self.waste["area"] == area].sort_values(
                by=["last_collection_days", "day_of_week"]
            )
            fills = sub["bin_fill_pct"].values
            deltas = np.diff(fills) if len(fills) > 1 else np.array([0.1])
            self._fill_delta_by_area[area] = list(np.abs(deltas[np.nonzero(deltas)])) or [0.05, 0.1, 0.15]

        self._tick = 0
        self._emergency_buffer: List[EmergencyEvent] = []
        self._state: Optional[Dict[str, Any]] = None

    def _hour_weight(self, hour: int, sample_hour: int) -> float:
        """Higher weight when CSV hour is close to current hour (circular)."""
        d = min((hour - sample_hour) % 24, (sample_hour - hour) % 24)
        return math.exp(-0.25 * d * d)

    def _sample_traffic_row_index(self, loc: int, hour: int) -> int:
        pool = self._traffic_idx[loc]
        rows = self.traffic.iloc[pool]
        weights = np.array([self._hour_weight(hour, int(h)) for h in rows["hour"].values])
        s = weights.sum()
        if s <= 0:
            return int(self._rng.choice(pool))
        weights = weights / s
        return int(self._rng.choices(list(pool), weights=weights, k=1)[0])

    def _sample_waste_row_index(self, loc: int) -> int:
        pool = self._waste_idx[loc]
        return int(self._rng.choice(pool))

    def _congestion_to_level(self, score: float) -> float:
        if self._t_max <= self._t_min:
            return 0.5
        v = (float(score) - self._t_min) / (self._t_max - self._t_min)
        return float(max(0.0, min(1.0, v)))

    def tick(self, weather_enc: int) -> None:
        self._tick += 1
        hour = datetime.now().hour

        for loc in range(1, self.N_LOC + 1):
            t_idx = self._sample_traffic_row_index(loc, hour)
            self._traffic_windows[loc].append(t_idx)
            row = self.traffic.iloc[t_idx]
            # Blend last window mean with new sample for smooth series
            cs = float(row["congestion_score"])
            if len(self._traffic_windows[loc]) >= 2:
                prev_idx = list(self._traffic_windows[loc])[-2]
                cs = 0.65 * cs + 0.35 * float(self.traffic.iloc[prev_idx]["congestion_score"])

            w_idx = self._sample_waste_row_index(loc)
            self._waste_windows[loc].append(w_idx)
            base_fill = float(self.waste.iloc[w_idx]["bin_fill_pct"])
            area = self._loc_to_area[loc]
            deltas = self._fill_delta_by_area.get(area, [0.08])
            delta = float(self._rng.choice(deltas))
            # Advance fill using empirical delta sign from data row ordering noise
            direction = self._rng.choice([-1.0, 1.0])
            fill = base_fill + direction * delta * (0.5 + 0.5 * math.sin(self._tick / 12.0))
            fill = max(0.0, min(100.0, fill))

            self._state["traffic_levels"][loc] = self._congestion_to_level(cs)
            self._state["waste_levels"][loc] = fill / 100.0
            self._state["traffic_row"][loc] = {
                "hour": int(row["hour"]),
                "day_enc": int(row["day_of_week"]),
                "junction_enc": int(row["junction"]),
                "weather_enc": int(row["weather"]),
                "vehicles": int(row["vehicles"]),
            }
            wr = self.waste.iloc[w_idx]
            self._state["waste_row"][loc] = {
                "area": int(wr["area"]),
                "day_of_week": int(wr["day_of_week"]),
                "population_density": float(wr["population_density"]),
                "last_collection_days": int(wr["last_collection_days"]),
                "bin_fill_pct": float(fill),
            }

        # Emergency: surface rare events from emergency_clean high_risk rows
        self._emergency_buffer.clear()
        em = self.emergency
        if len(em) > 0:
            risky = em[em["high_risk"] == 1]
            if len(risky) > 0 and self._rng.random() < 0.15:
                r = risky.sample(n=1, random_state=self._tick % 10000).iloc[0]
                zone = int(r["zone"])
                loc = next((l for l, z in self._loc_to_zone.items() if z == zone), self._rng.randint(1, 10))
                self._emergency_buffer.append(
                    EmergencyEvent(
                        event_type=self._rng.choice(list(EventType)),
                        severity=EmergencySeverity.HIGH,
                        nearest_response_unit=f"ERU-{self._rng.randint(1, 5)}",
                        timestamp=datetime.now(),
                        location_id=loc,
                    )
                )
            elif self._rng.random() < 0.03:
                loc = self._rng.randint(1, 10)
                self._emergency_buffer.append(
                    EmergencyEvent(
                        event_type=self._rng.choice(list(EventType)),
                        severity=EmergencySeverity.LOW,
                        nearest_response_unit=f"ERU-{self._rng.randint(1, 5)}",
                        timestamp=datetime.now(),
                        location_id=loc,
                    )
                )

        self._state["emergencies"] = list(self._emergency_buffer)
        self._state["weather_enc"] = weather_enc
        self._state["data_source"] = "real_data"

    def attach_state(self, state: Dict[str, Any]) -> None:
        self._state = state
        for _loc in range(1, self.N_LOC + 1):
            state.setdefault("traffic_row", {})
            state.setdefault("waste_row", {})

class StatisticalSimulator:
    """Fallback when CSVs are missing."""

    N_LOC = 10

    def __init__(self):
        self._rng = random.Random(123)
        self._state: Optional[Dict[str, Any]] = None

    def attach_state(self, state: Dict[str, Any]) -> None:
        self._state = state
        state.setdefault("traffic_row", {})
        state.setdefault("waste_row", {})
        for loc in range(1, self.N_LOC + 1):
            state["traffic_levels"][loc] = self._rng.uniform(0.1, 0.85)
            state["waste_levels"][loc] = self._rng.uniform(0.1, 0.85)
            state["traffic_row"][loc] = {
                "hour": datetime.now().hour,
                "day_enc": datetime.now().weekday(),
                "junction_enc": (loc - 1) % 8,
                "weather_enc": 0,
                "vehicles": 200,
            }
            state["waste_row"][loc] = {
                "area": (loc - 1) % 8,
                "day_of_week": datetime.now().weekday(),
                "population_density": 3000.0,
                "last_collection_days": 3,
                "bin_fill_pct": state["waste_levels"][loc] * 100,
            }

    def tick(self, weather_enc: int) -> None:
        assert self._state is not None
        s = self._state
        base = 0.45 + 0.1 * math.sin(datetime.now().hour / 24 * 2 * math.pi)
        for loc in range(1, self.N_LOC + 1):
            s["traffic_levels"][loc] = max(
                0.0,
                min(1.0, s["traffic_levels"][loc] + self._rng.uniform(-0.08, 0.08) * 0.5 + base * 0.1),
            )
            s["waste_levels"][loc] = max(
                0.0,
                min(1.0, s["waste_levels"][loc] + self._rng.uniform(0.0, 0.04)),
            )
            s["traffic_row"][loc]["weather_enc"] = weather_enc
            s["waste_row"][loc]["bin_fill_pct"] = s["waste_levels"][loc] * 100
        s["weather_enc"] = weather_enc
        s["data_source"] = "statistical_sim"
        s["emergencies"] = []


# --- Module state ---
_traffic_df = _safe_read_csv("traffic_clean.csv")
_waste_df = _safe_read_csv("waste_clean.csv")
_emergency_df = _safe_read_csv("emergency_clean.csv")

_engine: Any = None

city_state: Dict[str, Any] = {
    "traffic_levels": {i: 0.5 for i in range(1, 11)},
    "waste_levels": {i: 0.5 for i in range(1, 11)},
    "emergencies": [],
    "data_source": "statistical_sim",
    "weather_enc": 0,
    "traffic_row": {},
    "waste_row": {},
}


def _init_engine() -> None:
    global _engine
    if (
        _traffic_df is not None
        and _waste_df is not None
        and _emergency_df is not None
        and len(_traffic_df) > 50
        and len(_waste_df) > 10
    ):
        _engine = RealDataSimulator(_traffic_df, _waste_df, _emergency_df)
        print("[simulation] RealDataSimulator active (CSVs loaded).")
    else:
        _engine = StatisticalSimulator()
        print("[simulation] StatisticalSimulator fallback (CSVs missing or too small).")

    for k in city_state["traffic_levels"]:
        city_state["traffic_levels"][k] = 0.4
        city_state["waste_levels"][k] = 0.4
    city_state["traffic_row"] = {}
    city_state["waste_row"] = {}
    city_state["emergencies"] = []
    _engine.attach_state(city_state)


_init_engine()


def update_city_state() -> None:
    from api.services.external_data_service import get_integrated_data

    ext = get_integrated_data()
    weather_enc = int(ext.get("weather_enc", 0))
    _engine.tick(weather_enc)


async def run_simulation() -> None:
    while True:
        try:
            update_city_state()
            try:
                from api.db import persistence  # noqa: WPS433

                if persistence.is_db_ready():
                    persistence.persist_city_metrics(city_state)
            except ImportError:
                pass
            except Exception as ex:
                print(f"[simulation] persistence skipped: {ex}")
            # WebSocket broadcast
            try:
                from api.routes import ws as ws_mod  # noqa: WPS433

                await ws_mod.broadcast_state(get_current_state())
            except Exception:
                pass
        except Exception as e:
            print(f"Simulation error: {e}")
        await asyncio.sleep(5)


def get_current_state() -> Dict[str, Any]:
    return city_state


def get_feature_row_for_location(location_id: int) -> Tuple[Optional[dict], Optional[dict]]:
    """Expose latest sampled feature rows for ML-aligned explanations."""
    tr = city_state.get("traffic_row", {}).get(location_id)
    wr = city_state.get("waste_row", {}).get(location_id)
    return tr, wr
