from fastapi import APIRouter
from api.models.schemas import DecisionResponse
from api.services.decision_engine import generate_decisions

router = APIRouter(prefix="/system", tags=["System Decision"])

@router.get("/decision", response_model=DecisionResponse)
def get_system_decision():
    """Returns the unified decision response aggregating simulation, logic, and alerts."""
    return generate_decisions()
