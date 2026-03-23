from fastapi import APIRouter
from typing import List
from api.models.schemas import Alert
from api.services.alert_service import evaluate_alerts

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=List[Alert])
def get_alerts():
    return evaluate_alerts()
