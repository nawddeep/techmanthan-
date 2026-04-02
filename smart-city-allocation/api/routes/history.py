from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from api.services.history_service import get_full_history, get_history_trends
from api.utils.auth import get_current_user

router = APIRouter(prefix="/history", tags=["History Analytics"])


@router.get("/trends", dependencies=[Depends(get_current_user)])
def fetch_trends(limit: int = 15):
    return get_history_trends(limit)


@router.get("/full", dependencies=[Depends(get_current_user)])
def fetch_full_history(
    limit: int = Query(100, ge=1, le=5000),
    start: Optional[str] = None,
    end: Optional[str] = None,
):
    return get_full_history(limit=limit, start=start, end=end)
