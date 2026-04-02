from typing import List

from fastapi import APIRouter, Depends

from api.models.schemas import MapDataLocation, TrafficPredictionRequest, WastePredictionRequest
from api.services.alert_service import evaluate_alerts
from api.services.emergency_ml_service import predict_emergency_risk
from api.services.ml_service import predict_traffic, predict_waste
from api.services.simulation_service import get_current_state
from api.utils.auth import get_current_user

router = APIRouter(prefix="/map-data", tags=["Map Data"])

# Udaipur junctions — lat/lon approximations aligned to traffic_data.csv names
LOCATION_META = {
    1: ("Pratap Nagar", 24.5977, 73.7292),
    2: ("Sector 11 Chauraha", 24.6012, 73.7389),
    3: ("Madhuban", 24.5854, 73.7125),
    4: ("Hiran Magri", 24.5600, 73.7200),
    5: ("Bedla Road", 24.5500, 73.7000),
    6: ("Surajpol", 24.5833, 73.6833),
    7: ("Bhupalpura", 24.6000, 73.7000),
    8: ("Delhi Gate", 24.5764, 73.6839),
    9: ("Pratap Nagar", 24.5985, 73.7310),
    10: ("Madhuban", 24.5860, 73.7140),
}


@router.get("", response_model=List[MapDataLocation], dependencies=[Depends(get_current_user)])
def get_map_data():
    import datetime

    state = get_current_state()
    alerts = evaluate_alerts()
    now = datetime.datetime.now()
    weather_enc = int(state.get("weather_enc", 0))
    rc = 1 if state.get("data_source") == "real_data" else 0

    out: List[MapDataLocation] = []
    for loc_id in range(1, 11):
        name, lat, lon = LOCATION_META[loc_id]
        tr = state.get("traffic_row", {}).get(loc_id)
        wr = state.get("waste_row", {}).get(loc_id)
        if not tr:
            tr = {
                "hour": now.hour,
                "day_enc": now.weekday(),
                "junction_enc": (loc_id - 1) % 8,
                "weather_enc": weather_enc,
                "vehicles": 200,
            }
        if not wr:
            wr = {
                "area": (loc_id - 1) % 8,
                "day_of_week": now.weekday(),
                "population_density": 3000.0,
                "last_collection_days": 3,
                "bin_fill_pct": state["waste_levels"].get(loc_id, 0.5) * 100,
            }

        t_req = TrafficPredictionRequest(
            hour=int(tr["hour"]),
            day_enc=int(tr["day_enc"]),
            junction_enc=int(tr["junction_enc"]),
            weather_enc=int(tr["weather_enc"]),
            vehicles=int(tr["vehicles"]),
        )
        w_req = WastePredictionRequest(
            area=int(wr["area"]),
            day_of_week=int(wr["day_of_week"]),
            population_density=float(wr["population_density"]),
            last_collection_days=int(wr["last_collection_days"]),
            bin_fill_pct=float(wr["bin_fill_pct"]),
        )

        t_pred = predict_traffic(t_req)
        w_pred = predict_waste(w_req)

        tr_level = state["traffic_levels"].get(loc_id, 0)
        wa_level = state["waste_levels"].get(loc_id, 0)

        traffic_str = "high" if tr_level > 0.8 else ("medium" if tr_level > 0.4 else "low")
        waste_str = "high" if wa_level > 0.8 else ("medium" if wa_level > 0.4 else "low")

        loc_alerts = sum(1 for a in alerts if getattr(a, "location_id", None) == loc_id)

        zone = (loc_id - 1) % 5
        erisk, _, _ = predict_emergency_risk(zone, now.hour, now.weekday(), weather_enc, rc)

        out.append(
            MapDataLocation(
                location_id=loc_id,
                coordinates=[lat, lon],
                traffic_intensity=traffic_str,
                waste_status=waste_str,
                alerts_count=loc_alerts,
                junction_name=name,
                traffic_ml_label=t_pred.congestion_level,
                traffic_ml_probability=t_pred.numeric_score,
                waste_ml_label=w_pred.overflow_risk,
                waste_ml_probability=w_pred.numeric_score,
                emergency_risk_score=round(erisk, 2),
            )
        )

    return out
