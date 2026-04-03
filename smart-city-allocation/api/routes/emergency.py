from typing import List

from fastapi import APIRouter, Depends

from api.models.schemas import EmergencyEvent
from api.services.simulation_service import get_current_state
from api.utils.auth import get_current_user

router = APIRouter(prefix="/emergency", tags=["Emergency"])


@router.get("", response_model=List[EmergencyEvent])
def get_emergencies():
    state = get_current_state()
    return state["emergencies"]
