from fastapi import APIRouter
from typing import List
from api.models.schemas import EmergencyEvent
from api.services.simulation_service import get_current_state

router = APIRouter(prefix="/emergency", tags=["Emergency"])

@router.get("", response_model=List[EmergencyEvent])
def get_emergencies():
    state = get_current_state()
    return state["emergencies"]
