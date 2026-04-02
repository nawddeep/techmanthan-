import datetime
from typing import List

from api.models.schemas import (
    DecisionEmergency,
    DecisionResponse,
    DecisionTraffic,
    DecisionWaste,
    TrafficPredictionRequest,
    WastePredictionRequest,
)
from api.services.alert_service import evaluate_alerts
from api.services.cost_analysis_service import calculate_costs
from api.services.emergency_ml_service import explain_emergency, predict_emergency_risk
from api.services.ml_service import get_traffic_explanation, get_waste_explanation
from api.services.simulation_service import get_current_state


def calculate_city_health_score(
    max_traffic: float, max_waste: float, emergencies: list, alerts: list
) -> float:
    score = 100.0
    score -= min(35, max_traffic * 0.35)
    score -= min(30, max_waste * 0.30)
    score -= min(20, len(emergencies) * 5)
    score -= min(15, len(alerts) * 1.5)
    return round(max(0, score), 1)


def predict_overflow_eta(current_fill: float) -> str:
    avg_fill_rate_per_minute = 0.36
    if current_fill >= 100:
        return "OVERFLOW NOW"
    if current_fill < 50:
        return "Safe"
    minutes_left = (100 - current_fill) / avg_fill_rate_per_minute
    if minutes_left < 60:
        return f"~{int(minutes_left)} min"
    return f"~{minutes_left / 60:.1f} hrs"


def generate_decisions() -> DecisionResponse:
    state = get_current_state()
    raw_alerts = evaluate_alerts()
    alerts = [a.message for a in raw_alerts]

    traffic_vals = list(state["traffic_levels"].values())
    max_traffic = max(traffic_vals) * 100 if traffic_vals else 0

    if max_traffic > 85:
        t_status = "High"
    elif max_traffic >= 60:
        t_status = "Medium"
    else:
        t_status = "Low"

    waste_vals = list(state["waste_levels"].values())
    max_waste = max(waste_vals) * 100 if waste_vals else 0

    if max_waste > 90:
        w_risk = "Overflow"
    elif max_waste >= 70:
        w_risk = "High"
    else:
        w_risk = "Low"

    emergencies = state["emergencies"]
    e_type = "None"
    e_sev = "Low"
    for em in emergencies:
        sev = em.severity.value if hasattr(em.severity, "value") else str(em.severity)
        if sev == "high" or e_type == "None":
            et = em.event_type.value if hasattr(em.event_type, "value") else str(em.event_type)
            e_type = et.capitalize() if isinstance(et, str) else "Event"
            e_sev = sev.capitalize() if isinstance(sev, str) else "Low"
            if sev == "high":
                break

    actions: List[str] = []

    if max_traffic > 85:
        actions.append("Deploy traffic police at heavily congested junctions.")
    elif max_traffic >= 60:
        actions.append("Optimize traffic signals to improve flow.")

    if max_waste > 90:
        actions.append("Send immediate waste collection vehicle to critical zones.")
    elif max_waste >= 70:
        actions.append("Schedule waste collection for high-risk areas in next cycle.")

    if e_sev == "High":
        actions.append(f"Dispatch nearest emergency response unit immediately for {e_type}.")
    elif e_sev == "Medium":
        actions.append(f"Monitor {e_type} emergency and prepare response units.")

    if not actions:
        actions.append("Maintain routine city operations.")

    now = datetime.datetime.now()
    weather_enc = int(state.get("weather_enc", 0))

    # Worst traffic / waste locations by level
    worst_traffic_loc = max(state["traffic_levels"], key=lambda k: state["traffic_levels"][k])
    worst_waste_loc = max(state["waste_levels"], key=lambda k: state["waste_levels"][k])

    tr = state.get("traffic_row", {}).get(worst_traffic_loc) or {
        "hour": now.hour,
        "day_enc": now.weekday(),
        "junction_enc": (worst_traffic_loc - 1) % 8,
        "weather_enc": weather_enc,
        "vehicles": int((max_traffic / 100) * 400),
    }
    wr = state.get("waste_row", {}).get(worst_waste_loc) or {
        "area": (worst_waste_loc - 1) % 8,
        "day_of_week": now.weekday(),
        "population_density": 3500.0,
        "last_collection_days": 3,
        "bin_fill_pct": max_waste,
    }

    t_req = TrafficPredictionRequest(
        hour=int(tr["hour"]),
        day_enc=int(tr["day_enc"]),
        junction_enc=int(tr["junction_enc"]),
        weather_enc=int(tr["weather_enc"]),
        vehicles=int(tr["vehicles"]),
    )
    t_pred = 1 if max_traffic >= 60 else 0
    t_exp = get_traffic_explanation(t_req, max_traffic / 100, t_pred)

    w_req = WastePredictionRequest(
        area=int(wr["area"]),
        day_of_week=int(wr["day_of_week"]),
        population_density=float(wr["population_density"]),
        last_collection_days=int(wr["last_collection_days"]),
        bin_fill_pct=float(wr["bin_fill_pct"]),
    )
    w_pred = 1 if max_waste >= 70 else 0
    w_exp = get_waste_explanation(w_req, max_waste / 100, w_pred)

    # Emergency ML for all 10 zones (zone index 0-4 wraps)
    worst_zone = 1
    worst_risk = -1.0
    worst_high = False
    em_explain = None
    rc = 1 if state.get("data_source") == "real_data" else 0
    for loc in range(1, 11):
        zone = (loc - 1) % 5
        risk, high, conf = predict_emergency_risk(
            zone, now.hour, now.weekday(), weather_enc, rc
        )
        if risk > worst_risk:
            worst_risk = risk
            worst_zone = loc
            worst_high = high

    wz = (worst_zone - 1) % 5
    _, _, wconf = predict_emergency_risk(
        wz, now.hour, now.weekday(), weather_enc, rc
    )
    pred_int = 1 if worst_high else 0
    em_explain = explain_emergency(
        wz, now.hour, now.weekday(), weather_enc, rc, wconf, pred_int
    )

    if worst_high and e_sev == "Low":
        e_sev = "Medium"
    if worst_risk >= 4.0 and e_type == "None":
        e_type = "Risk Alert"

    emergencies_count = len(state.get("emergencies", []))
    roi_data = calculate_costs(max_traffic / 100, max_waste / 100, emergencies_count)
    city_health_score = calculate_city_health_score(
        max_traffic, max_waste, emergencies, raw_alerts
    )
    waste_overflow_eta = predict_overflow_eta(max_waste)

    try:
        from api.db import persistence

        if persistence.is_db_ready():
            persistence.persist_system_decision(
                city_health_score, max_traffic, max_waste, actions
            )
    except Exception:
        pass

    return DecisionResponse(
        traffic=DecisionTraffic(
            value=round(max_traffic, 1),
            status=t_status,
            explainability=t_exp,
            features=t_req,
        ),
        waste=DecisionWaste(
            value=round(max_waste, 1),
            risk=w_risk,
            explainability=w_exp,
            features=w_req,
            waste_overflow_eta=waste_overflow_eta,
        ),
        emergency=DecisionEmergency(
            type=e_type,
            severity=e_sev,
            worst_zone_id=worst_zone,
            worst_zone_risk_score=round(worst_risk, 2),
            explainability=em_explain,
        ),
        alerts=alerts,
        actions=actions,
        data_source=state.get("data_source", "simulated"),
        roi=roi_data,
        city_health_score=city_health_score,
    )
