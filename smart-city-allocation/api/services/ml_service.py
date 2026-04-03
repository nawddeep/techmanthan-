"""
ML inference service.

Column-order correctness guarantee
───────────────────────────────────
Training renames raw columns (junction → junction_enc, day_of_week → day_enc,
weather → weather_enc) before fitting the Pipeline.  The constants in
``api/models/ml_constants.py`` (TRAFFIC_FEATURES, WASTE_FEATURES) define the
canonical column order.  At inference time we always construct the DataFrame
from those constants (``df[TRAFFIC_FEATURES]``) so the column order is
deterministic and matches training, even if the input dict had a different key
ordering.  A ValueError is raised at load time if the model's expected features
diverge from our constants, making mismatches loud rather than silent.
"""
import os
import joblib
import pandas as pd
from api.models.schemas import (
    TrafficPredictionRequest, TrafficPredictionResponse,
    WastePredictionRequest, WastePredictionResponse,
    ModelExplainability,
)
from api.models.ml_constants import TRAFFIC_FEATURES, WASTE_FEATURES
from api.services.explainability_service import explain_prediction

_traffic_model = None
_waste_model = None


def _validate_model_features(model, expected_features: list, model_name: str) -> None:
    """
    Validate that the loaded model Pipeline's preprocessor expects the same
    columns we will pass at inference time.  Raises ValueError on mismatch so
    the problem surfaces immediately at startup rather than silently producing
    wrong predictions.
    """
    try:
        # scikit-learn Pipelines expose feature_names_in_ on the first step
        if hasattr(model, "named_steps"):
            first = list(model.named_steps.values())[0]
        else:
            first = model
        if hasattr(first, "feature_names_in_"):
            model_features = list(first.feature_names_in_)
            if model_features != expected_features:
                raise ValueError(
                    f"[{model_name}] Column mismatch!\n"
                    f"  Model expects: {model_features}\n"
                    f"  Constants say: {expected_features}\n"
                    f"  Update ml_constants.py or retrain the model."
                )
    except ValueError:
        raise
    except Exception:
        # Not all estimator types expose feature_names_in_ — skip silently
        pass


def load_models():
    global _traffic_model, _waste_model
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    traffic_model_path = os.path.join(base_dir, "traffic_model.pkl")
    waste_model_path = os.path.join(base_dir, "waste_model.pkl")

    try:
        if os.path.exists(traffic_model_path):
            _traffic_model = joblib.load(traffic_model_path)
            _validate_model_features(_traffic_model, TRAFFIC_FEATURES, "traffic")
            print("Traffic model loaded and validated.")
        if os.path.exists(waste_model_path):
            _waste_model = joblib.load(waste_model_path)
            _validate_model_features(_waste_model, WASTE_FEATURES, "waste")
            print("Waste model loaded and validated.")
    except ValueError as e:
        # Column mismatch — log loudly but allow startup to continue so
        # the rest of the API is still usable.
        print(f"[ml_service] FEATURE MISMATCH WARNING: {e}")
    except Exception as e:
        print(f"[ml_service] Error loading models: {e}")


def predict_traffic(req: TrafficPredictionRequest) -> TrafficPredictionResponse:
    if not _traffic_model:
        return TrafficPredictionResponse(
            congestion_level="low", numeric_score=0.1, suggested_action="Monitor"
        )
    # Build dict then select columns in canonical order to prevent silent
    # column-order mismatches at inference time.
    data = {
        "hour": req.hour,
        "day_enc": req.day_enc,
        "junction_enc": req.junction_enc,
        "weather_enc": req.weather_enc,
        "temperature_c": req.temperature_c,
        "vehicles": req.vehicles,
    }
    df = pd.DataFrame([data])[TRAFFIC_FEATURES]  # enforces column order
    pred = _traffic_model.predict(df)[0]
    prob = _traffic_model.predict_proba(df)[0].max()

    level = "high" if pred == 1 else "low"
    action = "Reroute traffic" if pred == 1 else "Normal operations"

    return TrafficPredictionResponse(
        congestion_level=level,
        numeric_score=float(prob),
        suggested_action=action,
    )


def predict_waste(req: WastePredictionRequest) -> WastePredictionResponse:
    if not _waste_model:
        return WastePredictionResponse(
            overflow_risk="low",
            priority_level="Low",
            numeric_score=0.1,
            optimized_collection_suggestion="Routine",
        )
    data = {
        "area": req.area,
        "day_of_week": req.day_of_week,
        "population_density": req.population_density,
        "last_collection_days": req.last_collection_days,
        "bin_fill_pct": req.bin_fill_pct,
    }
    df = pd.DataFrame([data])[WASTE_FEATURES]  # enforces column order
    pred = _waste_model.predict(df)[0]
    prob = _waste_model.predict_proba(df)[0].max()

    if pred == 1:
        risk, priority, suggestion = "high", "Urgent", "Dispatch collection immediately"
    else:
        risk, priority, suggestion = "low", "Low", "Routine schedule"

    return WastePredictionResponse(
        overflow_risk=risk,
        priority_level=priority,
        numeric_score=float(prob),
        optimized_collection_suggestion=suggestion,
    )


def get_traffic_explanation(req: TrafficPredictionRequest, prob: float, pred: int):
    if not _traffic_model:
        return None
    data = {
        "hour": req.hour,
        "day_enc": req.day_enc,
        "junction_enc": req.junction_enc,
        "weather_enc": req.weather_enc,
        "temperature_c": req.temperature_c,
        "vehicles": req.vehicles,
    }
    df = pd.DataFrame([data])[TRAFFIC_FEATURES]
    exp_dict = explain_prediction(_traffic_model, df, "traffic", prob, pred)
    return ModelExplainability(**exp_dict)


def get_waste_explanation(req: WastePredictionRequest, prob: float, pred: int):
    if not _waste_model:
        return None
    data = {
        "area": req.area,
        "day_of_week": req.day_of_week,
        "population_density": req.population_density,
        "last_collection_days": req.last_collection_days,
        "bin_fill_pct": req.bin_fill_pct,
    }
    df = pd.DataFrame([data])[WASTE_FEATURES]
    exp_dict = explain_prediction(_waste_model, df, "waste", prob, pred)
    return ModelExplainability(**exp_dict)
