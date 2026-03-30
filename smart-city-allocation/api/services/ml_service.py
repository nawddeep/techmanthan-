import os
import joblib
import pandas as pd
from api.models.schemas import (
    TrafficPredictionRequest, TrafficPredictionResponse,
    WastePredictionRequest, WastePredictionResponse,
    ModelExplainability
)
from api.services.explainability_service import explain_prediction

_traffic_model = None
_waste_model = None

def load_models():
    global _traffic_model, _waste_model
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    traffic_model_path = os.path.join(base_dir, 'traffic_model.pkl')
    waste_model_path = os.path.join(base_dir, 'waste_model.pkl')
    
    try:
        if os.path.exists(traffic_model_path):
            _traffic_model = joblib.load(traffic_model_path)
            print("Traffic model loaded.")
        if os.path.exists(waste_model_path):
            _waste_model = joblib.load(waste_model_path)
            print("Waste model loaded.")
    except Exception as e:
        print(f"Error loading models: {e}")

def predict_traffic(req: TrafficPredictionRequest) -> TrafficPredictionResponse:
    if not _traffic_model:
        return TrafficPredictionResponse(
            congestion_level="low", numeric_score=0.1, suggested_action="Monitor"
        )
    df = pd.DataFrame([{
        'hour': req.hour,
        'day_enc': req.day_enc,
        'junction_enc': req.junction_enc,
        'weather_enc': req.weather_enc,
        'vehicles': req.vehicles
    }])
    pred = _traffic_model.predict(df)[0]
    prob = _traffic_model.predict_proba(df)[0].max()
    
    level = "high" if pred == 1 else "low"
    action = "Reroute traffic" if pred == 1 else "Normal operations"
    
    return TrafficPredictionResponse(
        congestion_level=level,
        numeric_score=float(prob),
        suggested_action=action
    )

def predict_waste(req: WastePredictionRequest) -> WastePredictionResponse:
    if not _waste_model:
        return WastePredictionResponse(
            overflow_risk="low", priority_level="Low", numeric_score=0.1, optimized_collection_suggestion="Routine"
        )
    df = pd.DataFrame([{
        'area': req.area,
        'day_of_week': req.day_of_week,
        'population_density': req.population_density,
        'last_collection_days': req.last_collection_days,
        'bin_fill_pct': req.bin_fill_pct
    }])
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
        optimized_collection_suggestion=suggestion
    )

def get_traffic_explanation(req: TrafficPredictionRequest, prob: float, pred: int):
    if not _traffic_model:
        return None
    df = pd.DataFrame([{
        'hour': req.hour,
        'day_enc': req.day_enc,
        'junction_enc': req.junction_enc,
        'weather_enc': req.weather_enc,
        'vehicles': req.vehicles
    }])
    exp_dict = explain_prediction(_traffic_model, df, "traffic", prob, pred)
    return ModelExplainability(**exp_dict)

def get_waste_explanation(req: WastePredictionRequest, prob: float, pred: int):
    if not _waste_model:
        return None
    df = pd.DataFrame([{
        'area': req.area,
        'day_of_week': req.day_of_week,
        'population_density': req.population_density,
        'last_collection_days': req.last_collection_days,
        'bin_fill_pct': req.bin_fill_pct
    }])
    exp_dict = explain_prediction(_waste_model, df, "waste", prob, pred)
    return ModelExplainability(**exp_dict)
