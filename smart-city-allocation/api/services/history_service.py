"""Historical trends — backed by SQLite history_snapshots + city_metrics."""
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from api.db.database import SessionLocal
from api.db import models
from api.db import persistence


def append_history(traffic: float, waste: float) -> None:
    """Legacy name — persistence handled in decision_engine via persist_system_decision."""
    if not persistence.is_db_ready():
        return
    # Primary path: system_decisions + history_snapshots written in persist_system_decision
    pass


import random

def get_history_trends(limit: int = 15) -> Dict[str, Any]:
    if not persistence.is_db_ready():
        return {**_fallback_trends(limit), "is_fallback": True}

    db: Session = SessionLocal()
    try:
        rows = (
            db.query(models.HistoryAggregate)
            .order_by(desc(models.HistoryAggregate.timestamp))
            .limit(max(limit, 5))
            .all()
        )
        rows = list(reversed(rows))
        if len(rows) < 2:
            return {**_fallback_trends(limit), "is_fallback": True}
        return {
            "timestamps": [r.timestamp.strftime("%H:%M:%S") for r in rows],
            "traffic": [float(r.traffic) for r in rows],
            "waste": [float(r.waste) for r in rows],
            "is_fallback": False,
        }
    finally:
        db.close()


def _fallback_trends(limit: int) -> Dict[str, Any]:
    # Return 15 points by default
    n = 15
    base_ts = datetime.now().timestamp()
    return {
        "timestamps": [(datetime.fromtimestamp(base_ts - (n - i) * 60)).strftime("%H:%M") for i in range(n)],
        "traffic": [45.0 + 10.0 * random.random() for _ in range(n)],
        "waste": [30.0 + 20.0 * random.random() for _ in range(n)],
    }


def get_full_history(
    limit: int = 100,
    start: Optional[str] = None,
    end: Optional[str] = None,
) -> List[Dict[str, Any]]:
    if not persistence.is_db_ready():
        return []

    db: Session = SessionLocal()
    try:
        q = db.query(models.CityMetric).order_by(desc(models.CityMetric.timestamp))
        if start:
            q = q.filter(models.CityMetric.timestamp >= datetime.fromisoformat(start))
        if end:
            q = q.filter(models.CityMetric.timestamp <= datetime.fromisoformat(end))
        rows = q.limit(limit).all()
        out: List[Dict[str, Any]] = []
        for r in rows:
            out.append(
                {
                    "id": r.id,
                    "timestamp": r.timestamp.isoformat() if r.timestamp else None,
                    "location_id": r.location_id,
                    "traffic_level": r.traffic_level,
                    "waste_level": r.waste_level,
                    "data_source": r.data_source,
                }
            )
        return out
    finally:
        db.close()
