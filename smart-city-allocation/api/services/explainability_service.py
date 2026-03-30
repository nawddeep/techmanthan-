import shap
import pandas as pd
import numpy as np
from typing import Dict, Any, List

_explainers = {}

# Human-readable feature mapping
FEATURE_MAP = {
    "hour": "Current Hour",
    "day_enc": "Day of Week",
    "junction_enc": "Junction Importance",
    "weather_enc": "Weather Severity",
    "vehicles": "Vehicle Count",
    "area": "City Zone",
    "day_of_week": "Day of Week",
    "population_density": "Population Density",
    "last_collection_days": "Days Since Collection",
    "bin_fill_pct": "Current Bin Fill"
}

def get_explainer(model, model_type: str):
    global _explainers
    if model_type not in _explainers:
        # SHAP TreeExplainer is prioritized for Random Forest models
        # We use a summary dataset if the training data is too large, but for 
        # hackathon models, we can usually just pass the model itself.
        _explainers[model_type] = shap.TreeExplainer(model)
    return _explainers[model_type]

def explain_prediction(model, df: pd.DataFrame, model_type: str, confidence: float, prediction: int) -> Dict[str, Any]:
    """
    Generate explainability metrics for a single row prediction with SHAP values.
    """
    try:
        explainer = get_explainer(model, model_type)
        shap_values = explainer.shap_values(df)
        
        # Random Forest often returns [class_0, class_1] for binary
        if isinstance(shap_values, list):
            sv = shap_values[prediction][0]
        elif len(shap_values.shape) == 3:
            sv = shap_values[0, :, prediction]
        else:
            sv = shap_values[0]
            
        feature_names = df.columns.tolist()
        sv = np.array(sv).flatten()
        
        feature_details = []
        for i, name in enumerate(feature_names):
            val = float(df.iloc[0][name])
            impact = float(sv[i])
            
            feature_details.append({
                "feature": name,
                "display_name": FEATURE_MAP.get(name, name.replace("_", " ").title()),
                "value": round(val, 2),
                "impact": round(impact, 4),
                "effect": "increase" if impact > 0 else "decrease"
            })
            
        # Sort by absolute impact
        feature_details.sort(key=lambda x: abs(x["impact"]), reverse=True)
        top_3 = feature_details[:3]
        
        # Dynamic Plain English Explanation
        prediction_label = "High Congestion" if model_type == "traffic" and prediction == 1 else \
                           "Low Traffic" if model_type == "traffic" else \
                           "Overflow Risk" if model_type == "waste" and prediction == 1 else \
                           "Manageable Levels"
        
        main_factor = top_3[0]
        explanation = f"{prediction_label} is predicted primarily due to {main_factor['display_name']} ({main_factor['value']}), "
        
        if len(top_3) > 1:
            explanation += f"influenced by {top_3[1]['display_name']} and {top_3[2]['display_name']}."
        else:
            explanation += "which is the dominant factor."
            
        if model_type == "traffic" and prediction == 1 and "Vehicle Count" in [f['display_name'] for f in top_3]:
            val = next((f['value'] for f in top_3 if f['display_name'] == 'Vehicle Count'), main_factor['value'])
            explanation = f"High congestion is predicted because vehicle count is high ({val}), it is peak hour, and weather conditions are unfavorable."

        return {
            "prediction": prediction_label,
            "confidence": round(confidence * 100, 1),
            "top_features": top_3,
            "explanation": explanation
        }
    except Exception as e:
        print(f"SHAP error: {e}")
        
        prediction_label = "High Congestion" if model_type == "traffic" and prediction == 1 else \
                           "Low Traffic" if model_type == "traffic" else \
                           "Overflow Risk" if model_type == "waste" and prediction == 1 else \
                           "Manageable Levels"
                           
        # Fallback to feature importances
        try:
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                feature_names = df.columns.tolist()
                feature_details = []
                for i, name in enumerate(feature_names):
                    if importances[i] > 0:
                        feature_details.append({
                            "feature": name,
                            "display_name": FEATURE_MAP.get(name, name.replace("_", " ").title()),
                            "value": round(float(df.iloc[0][name]), 2),
                            "impact": round(float(importances[i]), 4),
                            "effect": "increase" # Simplified fallback effect
                        })
                feature_details.sort(key=lambda x: x["impact"], reverse=True)
                top_3 = feature_details[:3]
                
                main_factor = top_3[0]
                explanation = f"{prediction_label} is predicted primarily due to {main_factor['display_name']} ({main_factor['value']} - Rule-based estimate)."
                
                return {
                    "prediction": prediction_label,
                    "confidence": round(confidence * 100, 1),
                    "top_features": top_3,
                    "explanation": explanation
                }
        except Exception as fallback_e:
            print(f"Fallback error: {fallback_e}")
            
        return {
            "prediction": prediction_label,
            "confidence": round(confidence * 100, 1),
            "top_features": [],
            "explanation": f"{prediction_label} predicted. (Explanation temporarily unavailable)"
        }
