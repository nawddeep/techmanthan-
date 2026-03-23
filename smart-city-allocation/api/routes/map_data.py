from fastapi import APIRouter
from typing import List
from api.models.schemas import MapDataLocation
from api.services.simulation_service import get_current_state
from api.services.alert_service import evaluate_alerts

router = APIRouter(prefix="/map-data", tags=["Map Data"])

coord_map = {
    1: [24.5854, 73.7125],
    2: [24.5880, 73.7150],
    3: [24.5900, 73.7200],
    4: [24.5800, 73.7100],
    5: [24.5750, 73.7050],
    6: [24.5950, 73.7250],
    7: [24.6000, 73.7300],
    8: [24.5700, 73.7000],
    9: [24.5650, 73.6900],
    10: [24.6050, 73.7350]
}

@router.get("", response_model=List[MapDataLocation])
def get_map_data():
    state = get_current_state()
    alerts = evaluate_alerts()
    map_data = []
    
    for loc_id in range(1, 11):
        tr_level = state["traffic_levels"].get(loc_id, 0)
        wa_level = state["waste_levels"].get(loc_id, 0)
        
        traffic_str = "high" if tr_level > 0.8 else ("medium" if tr_level > 0.4 else "low")
        waste_str = "high" if wa_level > 0.8 else ("medium" if wa_level > 0.4 else "low")
        loc_alerts = sum(1 for a in alerts if getattr(a, 'location_id', None) == loc_id)
        
        map_data.append(MapDataLocation(
            location_id=loc_id,
            coordinates=coord_map.get(loc_id, [0.0, 0.0]),
            traffic_intensity=traffic_str,
            waste_status=waste_str,
            alerts_count=loc_alerts
        ))
        
    return map_data
