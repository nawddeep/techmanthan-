from typing import List

from fastapi import APIRouter, Depends

from api.models.schemas import Alert
from api.services.alert_service import evaluate_alerts
from api.utils.auth import get_current_user

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=List[Alert])
def get_alerts():
    return evaluate_alerts()
