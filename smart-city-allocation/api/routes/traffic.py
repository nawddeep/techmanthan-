from fastapi import APIRouter
from api.models.schemas import TrafficPredictionRequest, TrafficPredictionResponse
from api.services.ml_service import predict_traffic

router = APIRouter(prefix="/predict", tags=["Traffic"])

@router.post("/traffic", response_model=TrafficPredictionResponse)
def get_traffic_prediction(request: TrafficPredictionRequest):
    return predict_traffic(request)
