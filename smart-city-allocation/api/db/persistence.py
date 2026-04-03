"""Write-through persistence from simulation and decision engine."""
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from api.db.database import SessionLocal, engine
from api.db import models

_db_ok = False


def is_db_ready() -> bool:
    global _db_ok
    if not _db_ok:
        # Auto-check if we haven't marked as ready yet
        _db_ok = ping_db()
    return _db_ok


def mark_ready() -> None:
    global _db_ok
    _db_ok = True


def persist_city_metrics(state: Dict[str, Any]) -> None:
    if not _db_ok:
        return
    ts = datetime.utcnow()
    src = state.get("data_source", "unknown")
    db: Session = SessionLocal()
    try:
        for loc, v in state.get("traffic_levels", {}).items():
            w = state.get("waste_levels", {}).get(loc, 0.0)
            row = models.CityMetric(
                timestamp=ts,
                location_id=int(loc),
                traffic_level=float(v),
                waste_level=float(w),
                data_source=str(src),
            )
            db.add(row)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def persist_emergency_event(
    zone: int, risk_score: float, high_risk: bool, event_type: str, severity: str
) -> None:
    if not _db_ok:
        return
    db: Session = SessionLocal()
    try:
        db.add(
            models.EmergencyEventRecord(
                timestamp=datetime.utcnow(),
                zone=zone,
                risk_score=risk_score,
                high_risk=high_risk,
                event_type=event_type,
                severity=severity,
            )
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def persist_system_decision(
    city_health_score: float,
    max_traffic: float,
    max_waste: float,
    actions: List[str],
) -> None:
    if not _db_ok:
        return
    db: Session = SessionLocal()
    try:
        db.add(
            models.SystemDecisionRecord(
                timestamp=datetime.utcnow(),
                city_health_score=city_health_score,
                max_traffic=max_traffic,
                max_waste=max_waste,
                actions_json=json.dumps(actions),
            )
        )
        db.add(
            models.HistoryAggregate(
                timestamp=datetime.utcnow(),
                traffic=max_traffic,
                waste=max_waste,
            )
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def ping_db() -> bool:
    try:
        from sqlalchemy import text

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
