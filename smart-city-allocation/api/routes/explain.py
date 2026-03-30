from fastapi import APIRouter, HTTPException
from api.models.schemas import TrafficPredictionRequest, WastePredictionRequest, ExplainResponse
from api.services.ml_service import predict_traffic, predict_waste, get_traffic_explanation, get_waste_explanation
import pandas as pd

router = APIRouter(prefix="/explain", tags=["Explainability"])

@router.post("/traffic", response_model=ExplainResponse)
async def explain_traffic(request: TrafficPredictionRequest):
    """
    Get detailed SHAP explanation for a traffic prediction.
    """
    try:
        # 1. Get prediction & confidence
        pred_res = predict_traffic(request)
        
        # 2. Get explanation
        # Convert numeric_score (0.0-1.0) and congestion_level (high/low)
        pred_int = 1 if pred_res.congestion_level == "high" else 0
        explanation = get_traffic_explanation(request, pred_res.numeric_score, pred_int)
        
        if not explanation:
            raise HTTPException(status_code=500, detail="Explanation service unavailable")
            
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/waste", response_model=ExplainResponse)
async def explain_waste(request: WastePredictionRequest):
    """
    Get detailed SHAP explanation for a waste prediction.
    """
    try:
        # 1. Get prediction & confidence
        pred_res = predict_waste(request)
        
        # 2. Get explanation
        pred_int = 1 if pred_res.overflow_risk == "high" else 0
        explanation = get_waste_explanation(request, pred_res.numeric_score if hasattr(pred_res, 'numeric_score') else 0.85, pred_int)
        
        if not explanation:
            raise HTTPException(status_code=500, detail="Explanation service unavailable")
            
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
