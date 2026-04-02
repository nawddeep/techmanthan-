"""Emergency risk model — loads emergency_model.pkl with SHAP explainability."""
from __future__ import annotations

import os
from typing import Any, Dict, Tuple

import joblib
import numpy as np
import pandas as pd

from api.models.schemas import ModelExplainability
from api.services.explainability_service import explain_prediction

_emergency_model = None


def load_emergency_model() -> None:
    global _emergency_model
    base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(base, "emergency_model.pkl")
    try:
        if os.path.exists(path):
            _emergency_model = joblib.load(path)
            print("Emergency model loaded.")
    except Exception as e:
        print(f"Emergency model load error: {e}")
        _emergency_model = None


def _underlying_clf(model):
    if hasattr(model, "named_steps") and "clf" in model.named_steps:
        return model.named_steps["clf"]
    return model


def predict_emergency_risk(
    zone: int,
    hour: int,
    day_of_week: int,
    weather: int,
    road_condition: int,
) -> Tuple[float, bool, float]:
    """
    Returns (risk_score 0-5 scale approx, high_risk bool, confidence 0-1).
    """
    df = pd.DataFrame(
        [
            {
                "zone": int(zone),
                "hour": int(hour),
                "day_of_week": int(day_of_week),
                "weather": int(weather),
                "road_condition": int(road_condition),
            }
        ]
    )

    if _emergency_model is not None:
        proba = _emergency_model.predict_proba(df)[0]
        pred = int(_emergency_model.predict(df)[0])
        conf = float(max(proba))
        # Map probability to 0-5 score for display
        risk_score = float(5.0 * proba[1] if len(proba) > 1 else proba[0])
        high = bool(pred == 1)
        return risk_score, high, conf

    # Rule-based fallback
    base = 1.0 + 0.3 * (zone % 3) + 0.05 * hour / 24.0
    if road_condition >= 2:
        base += 1.2
    if weather >= 2:
        base += 0.8
    risk_score = float(min(5.0, base))
    high = risk_score >= 3.5
    conf = 0.55
    return risk_score, high, conf


def explain_emergency(
    zone: int,
    hour: int,
    day_of_week: int,
    weather: int,
    road_condition: int,
    confidence: float,
    prediction: int,
) -> ModelExplainability | None:
    if _emergency_model is None:
        return None
    df = pd.DataFrame(
        [
            {
                "zone": zone,
                "hour": hour,
                "day_of_week": day_of_week,
                "weather": weather,
                "road_condition": road_condition,
            }
        ]
    )
    d = explain_prediction(_emergency_model, df, "emergency", confidence, prediction)
    return ModelExplainability(**d)
