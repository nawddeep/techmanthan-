from fastapi import APIRouter
from api.services.history_service import get_history_trends

router = APIRouter(prefix="/history", tags=["History Analytics"])

@router.get("/trends")
def fetch_trends(limit: int = 15):
    """Fetch historical trends for the dynamic charts."""
    return get_history_trends(limit)
