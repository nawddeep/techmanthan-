from fastapi import APIRouter, Depends, HTTPException

from api.models.schemas import ExplainResponse, TrafficPredictionRequest, WastePredictionRequest
from api.services.ml_service import get_traffic_explanation, get_waste_explanation, predict_traffic, predict_waste
from api.utils.auth import require_roles

router = APIRouter(prefix="/explain", tags=["Explainability"])


@router.post(
    "/traffic",
    response_model=ExplainResponse,
    dependencies=[Depends(require_roles(["admin"]))],
)
async def explain_traffic(request: TrafficPredictionRequest):
    try:
        pred_res = predict_traffic(request)
        pred_int = 1 if pred_res.congestion_level == "high" else 0
        explanation = get_traffic_explanation(request, pred_res.numeric_score, pred_int)
        if not explanation:
            raise HTTPException(status_code=500, detail="Explanation service unavailable")
        return explanation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/waste",
    response_model=ExplainResponse,
    dependencies=[Depends(require_roles(["admin"]))],
)
async def explain_waste(request: WastePredictionRequest):
    try:
        pred_res = predict_waste(request)
        pred_int = 1 if pred_res.overflow_risk == "high" else 0
        conf = pred_res.numeric_score if hasattr(pred_res, "numeric_score") else 0.85
        explanation = get_waste_explanation(request, conf, pred_int)
        if not explanation:
            raise HTTPException(status_code=500, detail="Explanation service unavailable")
        return explanation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
