from fastapi import APIRouter, Depends

from api.models.schemas import DecisionResponse
from api.services.decision_engine import generate_decisions
from api.utils.auth import get_current_user

router = APIRouter(prefix="/system", tags=["System Decision"])


@router.get(
    "/decision",
    response_model=DecisionResponse,
    summary="Unified city decision",
    dependencies=[Depends(get_current_user)],
)
def get_system_decision():
    return generate_decisions()
