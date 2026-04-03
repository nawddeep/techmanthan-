"""Compute model evaluation metrics from CSV holdout + loaded joblib models."""
from __future__ import annotations

import os
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

_BASE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
_DATA = os.path.join(_BASE, "data")

_cache: Dict[str, Any] | None = None


def _eval_classifier(name: str, model, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    pipe = model
    pred = pipe.predict(X_test)
    proba = pipe.predict_proba(X_test)[:, 1] if hasattr(pipe, "predict_proba") else None
    acc = float(accuracy_score(y_test, pred))
    prec = float(precision_score(y_test, pred, zero_division=0))
    rec = float(recall_score(y_test, pred, zero_division=0))
    f1 = float(f1_score(y_test, pred, zero_division=0))
    auc = float(roc_auc_score(y_test, proba)) if proba is not None else None
    cm = confusion_matrix(y_test, pred).tolist()
    clf = pipe.named_steps["clf"] if hasattr(pipe, "named_steps") else pipe
    fi: Dict[str, float] = {}
    if hasattr(clf, "feature_importances_"):
        cols = list(X.columns)
        imp = clf.feature_importances_
        for i, c in enumerate(cols[: len(imp)]):
            fi[c] = float(imp[i])
    return {
        "name": name,
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "roc_auc": auc,
        "confusion_matrix": cm,
        "feature_importance": fi,
    }


def build_xy_traffic(df: pd.DataFrame):
    d = df.rename(
        columns={"junction": "junction_enc", "day_of_week": "day_enc", "weather": "weather_enc"}
    )
    X = d[["hour", "day_enc", "junction_enc", "weather_enc", "temperature_c", "vehicles"]]
    y = d["high_congestion"]
    return X, y


def build_xy_waste(df: pd.DataFrame):
    X = df[
        ["area", "day_of_week", "population_density", "last_collection_days", "bin_fill_pct"]
    ]
    y = df["overflow_risk"]
    return X, y


def build_xy_emergency(df: pd.DataFrame):
    X = df[["zone", "hour", "day_of_week", "weather", "road_condition"]]
    y = df["high_risk"]
    return X, y


def get_model_stats() -> Dict[str, Any]:
    global _cache
    if _cache is not None:
        return _cache

    import joblib

    out: Dict[str, Any] = {"traffic": None, "waste": None, "emergency": None}

    try:
        tdf = pd.read_csv(os.path.join(_DATA, "traffic_clean.csv"))
        tm = joblib.load(os.path.join(_BASE, "traffic_model.pkl"))
        X, y = build_xy_traffic(tdf)
        out["traffic"] = _eval_classifier("traffic", tm, X, y)
    except Exception as e:
        out["traffic"] = {"error": str(e)}

    try:
        wdf = pd.read_csv(os.path.join(_DATA, "waste_clean.csv"))
        wm = joblib.load(os.path.join(_BASE, "waste_model.pkl"))
        X, y = build_xy_waste(wdf)
        out["waste"] = _eval_classifier("waste", wm, X, y)
    except Exception as e:
        out["waste"] = {"error": str(e)}

    try:
        edf = pd.read_csv(os.path.join(_DATA, "emergency_clean.csv"))
        em = joblib.load(os.path.join(_BASE, "emergency_model.pkl"))
        X, y = build_xy_emergency(edf)
        out["emergency"] = _eval_classifier("emergency", em, X, y)
    except Exception as e:
        out["emergency"] = {"error": str(e)}

    _cache = out
    return out
