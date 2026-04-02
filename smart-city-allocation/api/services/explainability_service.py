import shap
import pandas as pd
import numpy as np
from typing import Any, Dict, List

_explainers = {}

FEATURE_MAP = {
    "hour": "Current Hour",
    "day_enc": "Day of Week",
    "junction_enc": "Junction",
    "weather_enc": "Weather Severity",
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


def get_explainer(estimator: Any, model_type: str):
    global _explainers
    key = f"{model_type}_{id(estimator)}"
    if key not in _explainers:
        _explainers[key] = shap.TreeExplainer(estimator)
    return _explainers[key]


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
            feature_details.append(
                {
                    "feature": name.split("__")[-1] if "__" in name else name,
                    "display_name": FEATURE_MAP.get(
                        name.split("__")[-1], name.replace("__", " ").title()
                    ),
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

        main_factor = top_3[0]
        explanation = (
            f"{prediction_label} is driven mainly by {main_factor['display_name']} "
            f"({main_factor['value']})."
        )
        if len(top_3) > 1:
            explanation += f" Secondary: {top_3[1]['display_name']}, {top_3[2]['display_name']}."

        return {
            "prediction": prediction_label,
            "confidence": round(confidence * 100, 1),
            "top_features": top_3,
            "explanation": explanation,
        }
    except Exception as e:
        print(f"SHAP error: {e}")
        prediction_label = "Prediction"
        return {
            "prediction": prediction_label,
            "confidence": round(confidence * 100, 1),
            "top_features": [],
            "explanation": f"{prediction_label} (explanation unavailable: {e})",
        }
