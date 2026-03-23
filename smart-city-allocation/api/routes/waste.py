from fastapi import APIRouter
from api.models.schemas import WastePredictionRequest, WastePredictionResponse
from api.services.ml_service import predict_waste

router = APIRouter(prefix="/predict", tags=["Waste"])

@router.post("/waste", response_model=WastePredictionResponse)
def get_waste_prediction(request: WastePredictionRequest):
    return predict_waste(request)
