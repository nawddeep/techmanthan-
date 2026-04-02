from fastapi import APIRouter, Depends

from api.models.schemas import WastePredictionRequest, WastePredictionResponse
from api.services.ml_service import predict_waste
from api.utils.auth import require_roles

router = APIRouter(prefix="/predict", tags=["Waste"])


@router.post(
    "/waste",
    response_model=WastePredictionResponse,
    dependencies=[Depends(require_roles(["admin"]))],
)
def get_waste_prediction(request: WastePredictionRequest):
    return predict_waste(request)
