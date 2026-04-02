from fastapi import APIRouter, Depends

from api.services.model_stats_service import get_model_stats
from api.utils.auth import get_current_user

router = APIRouter(prefix="/models", tags=["Model Performance"])


@router.get("/stats", dependencies=[Depends(get_current_user)])
def model_stats():
    return get_model_stats()
