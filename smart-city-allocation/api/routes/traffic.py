from fastapi import APIRouter, Depends

from api.models.schemas import TrafficPredictionRequest, TrafficPredictionResponse
from api.services.ml_service import predict_traffic
from api.utils.auth import require_roles

router = APIRouter(prefix="/predict", tags=["Traffic"])


@router.post(
    "/traffic",
    response_model=TrafficPredictionResponse,
    dependencies=[Depends(require_roles(["admin"]))],
)
def get_traffic_prediction(request: TrafficPredictionRequest):
    return predict_traffic(request)
