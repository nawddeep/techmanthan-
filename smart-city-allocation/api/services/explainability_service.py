"""
SHAP explainability service.

Explainer Cache Design
──────────────────────
We cache ``shap.TreeExplainer`` instances keyed by the **Python object id**
of the underlying estimator plus its class name.  This means:

* First call per model → creates and caches the explainer (can take 0.5–2 s).
* Subsequent calls → returns the cached explainer instantly.
* Hot-reload / model swap → ``id()`` changes for the new object, so a fresh
  explainer is created and the old one is evicted.  Memory does not leak.

Using ``id()`` alone would be unsafe in some Python garbage-collector edge
cases (reuse of the same memory address for a different object), so we use
both ``id()`` and ``type(estimator).__name__`` as the cache key.
"""
import shap
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Tuple

# Cache: (id, class_name) → TreeExplainer
# Using a plain dict with composite keys gives us deterministic eviction when
# models are swapped (id changes) without the WeakKeyDictionary pitfall of
# keeping stale references alive longer than expected.
_explainer_cache: Dict[Tuple[int, str], shap.TreeExplainer] = {}

FEATURE_MAP = {
    "hour": "Current Hour",
    "day_enc": "Day of Week",
    "junction_enc": "Junction",
    "weather_enc": "Weather Severity",
    "temperature_c": "Temperature (°C)",
    "vehicles": "Vehicle Count",
    "area": "City Zone",
    "day_of_week": "Day of Week",
    "population_density": "Population Density",
    "last_collection_days": "Days Since Collection",
    "bin_fill_pct": "Current Bin Fill",
    "zone": "Zone",
    "weather": "Weather",
    "road_condition": "Road Condition",
}


def _cache_key(estimator: Any) -> Tuple[int, str]:
    return (id(estimator), type(estimator).__name__)


def _prepare_X(model: Any, df: pd.DataFrame):
    """Return (tree estimator, feature matrix as DataFrame for SHAP)."""
    if hasattr(model, "named_steps") and "prep" in model.named_steps:
        prep = model.named_steps["prep"]
        Xt = prep.transform(df)
        try:
            names = list(prep.get_feature_names_out())
        except Exception:
            names = [f"f{i}" for i in range(np.asarray(Xt).shape[1])]
        if hasattr(Xt, "columns"):
            X_df = Xt
        else:
            X_df = pd.DataFrame(np.asarray(Xt), columns=names)
        return model.named_steps["clf"], X_df
    return model, df


def get_explainer(estimator: Any, model_type: str) -> shap.TreeExplainer:
    """
    Return a cached TreeExplainer for *estimator*.

    The cache key is ``(id(estimator), classname)`` so a new estimator object
    (e.g. after hot-reload) always gets a fresh explainer and the old entry is
    never accessed again.  Old entries are evicted to keep memory bounded.
    """
    key = _cache_key(estimator)
    if key not in _explainer_cache:
        # Evict any stale entries whose class_name matches (handles hot-reload)
        stale = [k for k in _explainer_cache if k[1] == key[1] and k[0] != key[0]]
        for k in stale:
            del _explainer_cache[k]
        _explainer_cache[key] = shap.TreeExplainer(estimator)
    return _explainer_cache[key]


def explain_prediction(
    model: Any, df: pd.DataFrame, model_type: str, confidence: float, prediction: int
) -> Dict[str, Any]:
    try:
        clf, X_shap = _prepare_X(model, df)
        explainer = get_explainer(clf, model_type)
        shap_values = explainer.shap_values(X_shap)

        if isinstance(shap_values, list):
            sv = shap_values[prediction][0]
        elif len(np.array(shap_values).shape) == 3:
            sv = np.array(shap_values)[0, :, prediction]
        else:
            sv = np.array(shap_values)[0]

        feature_names = X_shap.columns.tolist() if hasattr(X_shap, "columns") else []
        sv = np.array(sv).flatten()

        feature_details: List[Dict[str, Any]] = []
        for i, name in enumerate(feature_names):
            val = float(X_shap.iloc[0, i])
            impact = float(sv[i])
            short = name.split("__")[-1] if "__" in name else name
            feature_details.append(
                {
                    "feature": short,
                    "display_name": FEATURE_MAP.get(short, name.replace("__", " ").title()),
                    "value": round(val, 2),
                    "impact": round(impact, 4),
                    "effect": "increase" if impact > 0 else "decrease",
                }
            )

        feature_details.sort(key=lambda x: abs(x["impact"]), reverse=True)
        top_3 = feature_details[:3]

        if model_type == "traffic":
            prediction_label = "High Congestion" if prediction == 1 else "Low Traffic"
        elif model_type == "waste":
            prediction_label = "Overflow Risk" if prediction == 1 else "Manageable Levels"
        elif model_type == "emergency":
            prediction_label = "High Emergency Risk" if prediction == 1 else "Normal Risk"
        else:
            prediction_label = "Prediction"

        if top_3:
            main = top_3[0]
            explanation = (
                f"{prediction_label} is driven mainly by {main['display_name']} "
                f"({main['value']})."
            )
            if len(top_3) > 1:
                explanation += (
                    f" Secondary: {top_3[1]['display_name']}"
                    + (f", {top_3[2]['display_name']}." if len(top_3) > 2 else ".")
                )
        else:
            explanation = f"{prediction_label} (no feature details available)."

        return {
            "prediction": prediction_label,
            "confidence": round(confidence * 100, 1),
            "top_features": top_3,
            "explanation": explanation,
        }

    except Exception as e:
        print(f"[explainability] SHAP error: {e}")
        prediction_label = "Prediction"
        return {
            "prediction": prediction_label,
            "confidence": round(confidence * 100, 1),
            "top_features": [],
            "explanation": f"{prediction_label} (explanation unavailable: {e})",
        }
